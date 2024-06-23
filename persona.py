from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.chatbot_db
conversations_collection = db.conversations

API_KEY = "UpOkmmQYhyW9N9GTh5akVHqIbsCuqPmz"

PERSONAS = {
    "customer_support": {
        "instructions": "You are a helpful customer support agent.",
        "allowed_topics": ["order", "refund", "shipping", "product", "help"]
    },
    "teacher": {
        "instructions": "You are a knowledgeable teacher.",
        "allowed_topics": ["education", "homework", "lesson", "study", "exam"]
    },
    "motivational_coach": {
        "instructions": "You are an encouraging motivational coach.",
        "allowed_topics": ["motivation", "goal", "success", "encouragement", "confidence"]
    }
}

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

def validate_response(response, allowed_topics):
    for topic in allowed_topics:
        if topic.lower() in response.lower():
            return True
    return False

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get("prompt")
    user_id = data.get("user_id")
    persona = data.get("persona")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    if persona not in PERSONAS:
        return jsonify({"error": "Invalid persona provided"}), 400

    try:
        history = list(conversations_collection.find({"user_id": user_id}).sort("_id"))
        
        persona_data = PERSONAS[persona]
        persona_instructions = persona_data["instructions"]
        allowed_topics = persona_data["allowed_topics"]

        messages = [{"role": "system", "content": persona_instructions}]
        for entry in history:
            messages.append({"role": "user", "content": entry["prompt"]})
            messages.append({"role": "assistant", "content": entry["response"]})
        messages.append({"role": "user", "content": prompt})

        ai_response = get_ai21_response(messages)
        
        if not validate_response(ai_response, allowed_topics):
            ai_response = "I'm sorry, but I can only assist with topics related to my persona. Please ask something relevant."

        conversation = {
            "user_id": user_id,
            "prompt": prompt,
            "response": ai_response,
            "persona": persona
        }
        conversations_collection.insert_one(conversation)

        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8009)
