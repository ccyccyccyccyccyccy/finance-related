import db as db
import yfinance as yf
import pandas as pd
from tqdm import tqdm
from pymongo.server_api import ServerApi


def seed_database():
    client, collection = db.connect_to_mongodb()
    stocks = pd.read_csv('sse_stock.csv')
    for index, row in tqdm(stocks.iterrows(), total=stocks.shape[0]):
        stock_code = row['SSE Code']
        validated = row['Validated']
        if validated == 0:
            try: 
                data= yf.Ticker(stock_code).history(start="2001-01-01", interval="1d",auto_adjust=True)
                documents = []
                for i in range(len(data)):
                    doc = db.StockTimeSeries(
                        timestamp= data.index[i].isoformat(),
                        ticker= stock_code,
                        open= float(data.iloc[i]["Open"]),
                        high= float(data.iloc[i]["High"]),
                        low= float(data.iloc[i]["Low"]),
                        close= float(data.iloc[i]["Close"]),
                        volume= float(data.iloc[i]["Volume"]))
                    documents.append(doc)
                if documents:
                    db.insert_multiple_stock_data(collection, documents)
                    stocks.at[index, 'Validated'] = 1
                    stocks.to_csv('sse_stock.csv', index=False)
                    #print(f"Inserted data for {stock_code}")
            except Exception as e:
                print(f"Error processing {stock_code}: {e}")
        else:
            print(f"Skipping {stock_code}, already validated.")

if __name__ == "__main__":
    seed_database()
    print("Database seeding completed.")
