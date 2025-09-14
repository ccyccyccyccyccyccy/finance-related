from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
import os
from pydantic import BaseModel, Json
from datetime import datetime

class StockTimeSeries(BaseModel):
    #TODO: decide which fields to keep
    timestamp: datetime
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    # dividendYield: float
    # splits: int

    

def connect_to_mongodb():
    # Load environment variables from .env file
    dotenv.load_dotenv()
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI not found in environment variables. Please set it in the .env file.")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['stock_data']
    collection = db['stocks']
    return client, collection

def insert_multiple_stock_data(collection, stock_data_list):
    stock_data_dicts = [stock_data.model_dump() for stock_data in stock_data_list]
    collection.insert_many(stock_data_dicts)

def insert_stock_data(collection, stock_data): #example
    stock_data_dict = stock_data.model_dump()
    collection.insert_one(stock_data_dict)

def delete_test_data(collection):
    collection.delete_many({"ticker": {"$regex": r".*TEST.*"}})  # Example for deleting a specific stock code

def get_unique_stock_codes(collection):
    unique_codes = collection.distinct("ticker")
    return unique_codes

def get_latest_stocks(collection): #for updating 
    unique_codes = collection.distinct("ticker")
    latest_stocks={}
    for code in unique_codes:
        latest_entry = collection.find({"ticker": code}).sort("timestamp", -1).limit(1)
        if latest_entry:
            latest_stocks[code] = latest_entry[0]
    return latest_stocks

def get_stock_data(collection, start_date, end_date, ticker, fields=None):
    if fields:
        projection = {field: 1 for field in fields}
    else:
        projection = None

    stock_data = collection.find({
        "ticker": ticker,
        "timestamp": {"$gte": start_date, "$lte": end_date}
        }, projection)

    return stock_data

def insert_test_data(collection):
    #stock_codes = ["600000.TEST1", "600001.TEST2", "600002.TEST3"]
    stock_codes = ["600000.TEST1", "600001.TEST2", "600002.TEST3", "600000.TEST4", "600001.TEST5"]
    #stock_codes = ["600000.TEST6", "600001.TEST7", "600002.TEST8", "600003.TEST9", "600004.TEST10"]
    import random
    from datetime import datetime, timedelta
    for code in stock_codes:
        for i in range(10):
            stock_data = StockTimeSeries(
                timestamp=datetime.now() - timedelta(days=i),
                ticker=code,
                high=random.uniform(100, 200),
                low=random.uniform(50, 100),
                open=random.uniform(80, 150),
                close=random.uniform(90, 180),
                volume=random.randint(1000, 5000)
            )
            insert_stock_data(collection, stock_data)
    print("Test data inserted.")

def testing():
    client, collection = connect_to_mongodb()
    #delete_test_data(collection)
    #print("Test data deleted.")
    #insert_test_data(collection)
    # latest_stocks= get_latest_stocks(collection)
    # print("Latest stocks:", latest_stocks)
    stock_data = get_stock_data(collection, datetime(2025, 8, 1), datetime(2025, 8, 5), "688707.SS", ["timestamp", "ticker", "open", "high", "low", "close", "volume"])

    for data in stock_data:
        print("Stock data:", data)

    #delete_test_data(collection)
    #print("Test data deleted.")
    # unique_codes = collection.distinct("ticker")
    # for code in unique_codes:
    #     print("Unique stock code:", code)
    client.close()

if __name__ == "__main__":
    testing()