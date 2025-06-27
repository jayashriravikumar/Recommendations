import pandas as pd
import pickle
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model
with open(os.path.join(BASE_DIR, "stock_forecast_model.pkl"), "rb") as f:
    model = pickle.load(f)

# Load features and stock
features_df = pd.read_pickle(os.path.join(BASE_DIR, "daily_features.pkl"))
stock_df = pd.read_csv(os.path.join(BASE_DIR, "stock.csv"))

features_df = features_df.sort_values(['pro_id', 'cdate'])

# Prediction
def get_stock_forecast():
    future_preds = []
    for pid in stock_df['pro_id'].unique():
        recent = features_df[features_df['pro_id'] == pid].sort_values('cdate').tail(1)
        if recent.empty:
            continue
        base = recent.iloc[0]
        pred_sum = 0
        for i in range(1, 8):
            dow = (base['cdate'] + timedelta(days=i)).dayofweek
            row = pd.DataFrame([{
                'dayofweek': dow,
                'is_weekend': 1 if dow >= 5 else 0,
                'lag_1': base['qty_sold'],
                'rolling_7': base['rolling_7'],
                'rolling_14': base['rolling_14'],
                'rolling_28': base['rolling_28']
            }])
            pred = model.predict(row)[0]
            pred_sum += pred

        future_preds.append({
            "pro_id": pid,
            "forecasted_demand_7d": round(pred_sum, 0)
        })

    pred_df = pd.DataFrame(future_preds)
    final = stock_df.merge(pred_df, on="pro_id", how="left")
    final['forecasted_demand_7d'] = final['forecasted_demand_7d'].fillna(0)
    final['stockout_risk'] = final['forecasted_demand_7d'] > final['qty']
    final['remaining_stock'] = final['qty'] - final['forecasted_demand_7d']

    final['remaining_stock'] = final['remaining_stock'].round(0).astype(int)
    result = final[final['stockout_risk'] == True]

    return result[['pro_id', 'qty', 'forecasted_demand_7d', 'remaining_stock', 'stockout_risk']]