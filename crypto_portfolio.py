from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

crypto_exchange_db = client['CryptoExchangeDB']
user_portfolio_db = client['UserPortfolioDB']

cryptocurrencies_collection = crypto_exchange_db['Cryptocurrencies']
user_portfolios_collection = user_portfolio_db['UserPortfolios']

cryptocurrencies_data = [
    {"crypto_id": 1, "name": "Bitcoin", "symbol": "BTC", "price_usd": 30000},
    {"crypto_id": 2, "name": "Ethereum", "symbol": "ETH", "price_usd": 2000},
    {"crypto_id": 3, "name": "Cardano", "symbol": "ADA", "price_usd": 1},
    {"crypto_id": 4, "name": "Solana", "symbol": "SOL", "price_usd": 40},
    {"crypto_id": 5, "name": "Ripple", "symbol": "XRP", "price_usd": 0.5},
    {"crypto_id": 6, "name": "Polkadot", "symbol": "DOT", "price_usd": 20},
    {"crypto_id": 7, "name": "Chainlink", "symbol": "LINK", "price_usd": 25},
    {"crypto_id": 8, "name": "Litecoin", "symbol": "LTC", "price_usd": 150},
    {"crypto_id": 9, "name": "Stellar", "symbol": "XLM", "price_usd": 0.1},
    {"crypto_id": 10, "name": "Dogecoin", "symbol": "DOGE", "price_usd": 0.07}
]

user_portfolios_data = [
    {"user_id": 1, "name": "Ram", "holdings": [{"crypto_id": 1, "amount": 0.5}, {"crypto_id": 2, "amount": 10}]},
    {"user_id": 2, "name": "Manan", "holdings": [{"crypto_id": 3, "amount": 1000}, {"crypto_id": 4, "amount": 50}]},
    {"user_id": 3, "name": "Lakshay", "holdings": [{"crypto_id": 2, "amount": 5}, {"crypto_id": 5, "amount": 2000}]},
    {"user_id": 4, "name": "Krish", "holdings": [{"crypto_id": 6, "amount": 10}, {"crypto_id": 7, "amount": 8}]},
    {"user_id": 5, "name": "Anmol", "holdings": [{"crypto_id": 8, "amount": 2}, {"crypto_id": 9, "amount": 5000}]},
    {"user_id": 6, "name": "Anuj", "holdings": [{"crypto_id": 10, "amount": 10000}, {"crypto_id": 1, "amount": 0.1}]},
    {"user_id": 7, "name": "Prabal", "holdings": [{"crypto_id": 4, "amount": 15}, {"crypto_id": 3, "amount": 700}]},
    {"user_id": 8, "name": "Aman", "holdings": [{"crypto_id": 5, "amount": 3000}, {"crypto_id": 7, "amount": 20}]},
    {"user_id": 9, "name": "Manit", "holdings": [{"crypto_id": 2, "amount": 3}, {"crypto_id": 9, "amount": 10000}]},
    {"user_id": 10, "name": "Dev", "holdings": [{"crypto_id": 6, "amount": 7}, {"crypto_id": 8, "amount": 1}]}
]

cryptocurrencies_collection.insert_many(cryptocurrencies_data)
user_portfolios_collection.insert_many(user_portfolios_data)


