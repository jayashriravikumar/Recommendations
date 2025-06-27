import pandas as pd
import os
import lightgbm as lgb
import pickle


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
purchase_df = pd.read_csv(os.path.join(BASE_DIR, "new_purchase.csv"))
purchase_df['cdate'] = pd.to_datetime(purchase_df['cdate'], dayfirst=True)

# Step 1: Aggregate
features_df = purchase_df.groupby(['pro_id', purchase_df['cdate'].dt.date]) \
    .size().reset_index(name='qty_sold')
features_df['cdate'] = pd.to_datetime(features_df['cdate'])

# Step 2: Feature Engineering
features_df = features_df.sort_values(['pro_id', 'cdate'])
features_df['dayofweek'] = features_df['cdate'].dt.dayofweek
features_df['is_weekend'] = features_df['dayofweek'].isin([5, 6]).astype(int)
features_df['lag_1'] = features_df.groupby('pro_id')['qty_sold'].shift(1)
features_df['rolling_7'] = features_df.groupby('pro_id')['qty_sold'].transform(lambda x: x.shift(1).rolling(7).mean())
features_df['rolling_14'] = features_df.groupby('pro_id')['qty_sold'].transform(lambda x: x.shift(1).rolling(14).mean())
features_df['rolling_28'] = features_df.groupby('pro_id')['qty_sold'].transform(lambda x: x.shift(1).rolling(28).mean())
features_df['target'] = features_df.groupby('pro_id')['qty_sold'].shift(-1)

features_df.dropna(inplace=True)
features_df.to_pickle(os.path.join(BASE_DIR, "daily_features.pkl"))
print("✅ Features saved to daily_features.pkl")

features_df = pd.read_pickle(os.path.join(BASE_DIR, "daily_features.pkl"))

features = ['dayofweek', 'is_weekend', 'lag_1', 'rolling_7', 'rolling_14', 'rolling_28']
X = features_df[features]
y = features_df['target']

model = lgb.LGBMRegressor(n_estimators=100)
model.fit(X, y)

with open(os.path.join(BASE_DIR, "stock_forecast_model.pkl"), "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to stock_forecast_model.pkl")
