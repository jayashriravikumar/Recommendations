import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 🔁 Import forecast from your stock_pred.py
from stock_pred import get_stock_forecast

# 1️⃣ Run the forecast function (already using 20-06-2025 as reference in stock_pred.py)
forecast_df = get_stock_forecast()

# 2️⃣ Load the purchase data
df = pd.read_csv("new_purchase.csv", parse_dates=["cdate"], dayfirst=True)
df.columns = df.columns.str.lower()

# 3️⃣ Define the actual 7-day window (next 7 days after prediction date)
start_date = datetime.strptime("21-06-2025", "%d-%m-%Y")
end_date = datetime.strptime("27-06-2025", "%d-%m-%Y")

# 4️⃣ Filter and aggregate actual sales
filtered = df[(df['cdate'] >= start_date) & (df['cdate'] <= end_date)]
actual_7day_demand = filtered.groupby("pro_id").size().reset_index(name="actual_demand_7d")
actual_7day_demand.columns = ["pro_id", "actual_demand_7d"]

# 5️⃣ Join predictions with actuals
comparison = pd.merge(forecast_df, actual_7day_demand, on="pro_id", how="inner")

# 6️⃣ Evaluate model
mae = mean_absolute_error(comparison['actual_demand_7d'], comparison['forecasted_demand_7d'])
rmse = np.sqrt(mean_squared_error(comparison['actual_demand_7d'], comparison['forecasted_demand_7d']))
r2 = r2_score(comparison['actual_demand_7d'], comparison['forecasted_demand_7d'])

# 7️⃣ Display results
print("📈 Evaluation Results:")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

# Display side-by-side forecast vs actual demand
print("\n📦 Forecast vs Actual Demand (21–27 June 2025):\n")
print(comparison[['pro_id', 'forecasted_demand_7d', 'actual_demand_7d']].to_string(index=False))

