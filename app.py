from flask import Flask, request, jsonify
from recommender import recommend_from_model
from stock_pred import get_stock_forecast
import csv
import datetime
import os
import pandas as pd

print("📦 Flask app is starting...")

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
products_df = pd.read_csv(os.path.join(BASE_DIR, "Products.csv"))


# @app.route("/recommend", methods=["GET"])
# def get_recommendations():
#     user_id = request.args.get("user_id", type=int)
#     if user_id is None:
#         return jsonify({"error": "user_id parameter is required"}), 400

#     results = recommend_from_model(user_id)
#     return jsonify({
#         "user_id": user_id,
#         "recommendations": results
#     })


LOG_PATH = os.path.join("logs", "recommendation_logs.csv")

@app.route("/recommend", methods=["GET"])
def get_recommendations():
    user_id = request.args.get("user_id", type=int)
    if user_id is None:
        return jsonify({"error": "user_id parameter is required"}), 400

    results = recommend_from_model(user_id)

    # Log recommendations to CSV
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        for rec in results:
            writer.writerow([timestamp, user_id, rec['product_id'], rec['title'], rec['category'], "recommended"])

    return jsonify({
        "user_id": user_id,
        "recommendations": results
    })

CLICK_LOG_PATH = os.path.join("logs", "click_logs.csv")

@app.route("/track_click", methods=["POST"])
def track_click():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    action = data.get("action", "clicked")  # could be 'clicked', 'purchased', etc.
    
    # Optionally enrich product info
    product = products_df[products_df['id'] == product_id]
    if not product.empty:
        title = product.iloc[0]['title']
        category = product.iloc[0]['single_category']
    else:
        title, category = "Unknown", "Unknown"

    timestamp = datetime.datetime.now().isoformat()
    with open(CLICK_LOG_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, user_id, product_id, title, category, action])

    return jsonify({"message": "Click tracked."}), 200



@app.route("/forecast_stock", methods=["GET"])
def forecast_stock():
    df = get_stock_forecast()
    df.columns = ['pro_id', 'current_stock', 'forecasted_demand_7d', 'remaining_stock', 'stockout_risk']
    return jsonify(df.to_dict(orient='records'))



if __name__ == "__main__":
    print("🚀 Flask app running on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

