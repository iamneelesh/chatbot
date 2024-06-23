from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017"  
client = MongoClient(MONGO_URI)
db = client.chatbot_db
collection = db.conversations

API_KEY = "UpOkmmQYhyW9N9GTh5akVHqIbsCuqPmz"

def get_ai21_response(prompt):
    url = "https://api.ai21.com/studio/v1/chat/completions"

    res = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json={
        'model': 'jamba-instruct',
        'messages': [
            {
                "role": "user",
                "content": prompt
            }
        ],
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

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        ai_response = get_ai21_response(prompt)
        
      
        conversation = {
            "prompt": prompt,
            "response": ai_response
        }
        collection.insert_one(conversation)

        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8009)

if __name__ == '_main_':
    app.run(debug=True)
