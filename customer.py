from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
import re

app = Flask(__name__)


MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.chatbot_db
orders_collection = db.orders


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

def handle_order_query(prompt, user_id):
    order_id_match = re.search(r'\b\d{5}\b', prompt)
    if order_id_match:
        order_id = order_id_match.group()
        order = orders_collection.find_one({"order_id": order_id, "user_id": user_id})
        if order:
            return f"Your order {order_id} is currently {order['status']}. It was shipped on {order['shipping_date']} and is expected to be delivered by {order['delivery_date']}."
        else:
            return f"I couldn't find any order with ID {order_id} for your account."
    return None

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get("prompt")
    user_id = data.get("user_id")
    
    persona_context = {
        "name": "customer_support",
        "allowed_topics": ["order", "faq"]
    }

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        allowed_topics = persona_context.get("allowed_topics", [])

       
        if "order" in allowed_topics:
            response = handle_order_query(prompt, user_id)
            if response:
                return jsonify({"response": response})

       
        if "faq" in allowed_topics:
            
            return jsonify({"response": "FAQ handling is not implemented yet."})

        
        messages = [{"role": "user", "content": prompt}]
        ai_response = get_ai21_response(messages)
        
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8009)

















#     "prompt": "What is the status of order 12345?",
#     "user_id": "user123"


