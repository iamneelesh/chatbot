from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)


MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)


crypto_exchange_db = client['CryptoExchangeDB']
user_portfolio_db = client['UserPortfolioDB']
query_log_db = client['QueryLogDB']


cryptocurrencies_collection = crypto_exchange_db['Cryptocurrencies']
user_portfolios_collection = user_portfolio_db['UserPortfolios']
queries_collection = query_log_db['Queries']

def serialize_object_id(data):
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    elif isinstance(data, dict):                        #BSon to string conversion so the _id feild is converted to string
        if '_id' in data:
            data['_id'] = str(data['_id'])
    return data

def calculate_portfolio_value(holdings, crypto_dict):
    total_value = 0
    for holding in holdings:
        crypto = crypto_dict.get(holding['crypto_id'])
        if crypto:
            total_value += holding['amount'] * crypto['price_usd']
    return total_value

@app.route('/portfolio', methods=['POST'])
def portfolio():
    try:
        data = request.json
        user_id = data.get("user_id")
        query = data.get("query")

        if not user_id:
            return jsonify({"error": "No user_id provided"}), 400
        
        if not query:
            return jsonify({"error": "No query provided"}), 400

        
        user = user_portfolios_collection.find_one({"user_id": user_id})
        if not user:
            return jsonify({"error": "User not found"}), 404

        holdings = user['holdings']
        crypto_ids = [holding['crypto_id'] for holding in holdings]
        cryptos = cryptocurrencies_collection.find({"crypto_id": {"$in": crypto_ids}})
        crypto_dict = {crypto['crypto_id']: crypto for crypto in cryptos}

        if "portfolio value" in query.lower():
            total_value = calculate_portfolio_value(holdings, crypto_dict)
            response = {
                "total_portfolio_value_usd": total_value,
                "response": f"Your total portfolio value is ${total_value:.2f} USD"
            }

        elif "top holdings" in query.lower():
            user_holdings = []
            for holding in holdings:
                crypto = crypto_dict.get(holding['crypto_id'])
                if crypto:
                    user_holdings.append({
                        "crypto_name": crypto['name'],
                        "crypto_symbol": crypto['symbol'],
                        "amount": holding['amount'],
                        "price_usd": crypto['price_usd'],
                        "value_usd": holding['amount'] * crypto['price_usd']
                    })
            user_holdings.sort(key=lambda x: x["value_usd"], reverse=True)
            response = {
                "top_holdings": user_holdings[:5],  
                "response": "Here are your top holdings"
            }

        elif "holdings of" in query.lower():
            crypto_name = query.split("holdings of")[-1].strip()
            user_holdings = []
            for holding in holdings:
                crypto = crypto_dict.get(holding['crypto_id'])
                if crypto and crypto_name.lower() in crypto['name'].lower():
                    user_holdings.append({
                        "crypto_name": crypto['name'],
                        "crypto_symbol": crypto['symbol'],
                        "amount": holding['amount'],
                        "price_usd": crypto['price_usd'],
                        "value_usd": holding['amount'] * crypto['price_usd']
                    })
            response = {
                "specific_holdings": user_holdings,
                "response": f"Here are your holdings for {crypto_name}"
            }

        elif "portfolio details" in query.lower():
            user_holdings = []
            for holding in holdings:
                crypto = crypto_dict.get(holding['crypto_id'])
                if crypto:
                    user_holdings.append({
                        "crypto_name": crypto['name'],
                        "crypto_symbol": crypto['symbol'],
                        "amount": holding['amount'],
                        "price_usd": crypto['price_usd'],
                        "value_usd": holding['amount'] * crypto['price_usd']
                    })
            response = {
                "holdings": user_holdings,
                "response": "Here are your portfolio details"
            }

        else:
            response = {
                "response": "Query not recognized. Please ask about 'portfolio value', 'top holdings', 'portfolio details', or 'holdings of [cryptocurrency]'."
            }

     
        queries_collection.insert_one(serialize_object_id(response))

        return jsonify(serialize_object_id(response))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8009)

#serialistion of objectid was not happening thats why used bson