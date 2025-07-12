from flask import Flask, jsonify, request, send_file
import pandas as pd

app = Flask(__name__)

# Home route
@app.route('/')
def ebitda():
    query = request.args.get('Sector')
    if query:
        df = pd.read_csv(r"data\constituents-financials_csv.csv")
        return jsonify(df[df['Sector'] == query]["EBITDA"].tolist()), 200


# Example of a JSON response
@app.route('/Sector', methods=['GET'])
def get_sectors():
    df = pd.read_csv(r"data\constituents-financials_csv.csv")
    return jsonify(df["Sector"].unique().tolist()), 200

@app.route("/download")
def download():
    return send_file(r"data\constituents-financials_csv.csv", as_attachment=True), 200

if __name__ == '__main__':
    app.run(debug=True)
