from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)


MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.chatbot_db


@app.route('/add_order', methods=['POST'])
def add_order():
    try:
        orders_collection = db.orders
        order_data = request.json
        
        result = orders_collection.insert_one(order_data)
        
        return jsonify({"message": "Order added successfully", "inserted_id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8010)
