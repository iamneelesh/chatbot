from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.chatbot_db
conversations_collection = db.conversations

API_KEY = "UpOkmmQYhyW9N9GTh5akVHqIbsCuqPmz"

def get_ai21_response(messages):
    url = "https://api.ai21.com/studio/v1/chat/completions"

    res = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json={
        'model': 'jamba-instruct',
        'messages': messages,
        "max_tokens": 200,
        "temperature": 1,
        "top_p": 1,
        "stop": None,
    })

    return res.json()["choices"][0]["message"]["content"]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get("prompt")
    user_id = data.get("user_id")  

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
    
        history = list(conversations_collection.find({"user_id": user_id}).sort("_id"))
        
      
        messages = []
        for entry in history:
            messages.append({"role": "user", "content": entry["prompt"]})
            messages.append({"role": "assistant", "content": entry["response"]})
        messages.append({"role": "user", "content": prompt})

     
        ai_response = get_ai21_response(messages)
        
        conversation = {
            "user_id": user_id,
            "prompt": prompt,
            "response": ai_response
        }
        conversations_collection.insert_one(conversation)

        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8009)
