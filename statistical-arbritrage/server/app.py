from flask import Flask, jsonify, request
import db
import re
from bson import json_util
from datetime import datetime

app = Flask(__name__)
client, collection = db.connect_to_mongodb()

@app.route('/stocks', methods=['GET'])
def stock_data():
    start_date = request.args.get('StartDate')
    end_date = request.args.get('EndDate')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', start_date) or not re.match(r'^\d{4}-\d{2}-\d{2}$', end_date):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    ticker = request.args.get('Ticker')
    fields = request.args.getlist('Fields')
    if not fields:
        #return all
        fields = ["timestamp", "ticker", "open", "high", "low", "close", "volume"]
    if start_date and end_date and ticker:
        try:
            result= db.get_stock_data(collection, start_date, end_date, ticker, fields=fields)
            data = list(result)
            return json_util.dumps(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Missing required parameters"}), 400

@app.route("/unique_codes", methods=['GET'])
def unique_codes():
    try:
        codes = db.get_unique_stock_codes(collection)
        return jsonify(codes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
