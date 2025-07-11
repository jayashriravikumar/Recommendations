# #!/bin/bash
# mkdir -p /app/logs
# touch /app/logs/recommendation_logs.csv /app/logs/click_logs.csv

# echo "📅 Starting cron..."
# cron
# pgrep cron || echo "❌ cron did not start"

# touch /var/log/cron.log /var/log/test_cron.log
# echo "📋 Loaded cron jobs:"
# cat /etc/cron.d/model-cron

# echo "🧠 Running model training on container start..."
# python3 /app/model.py

# echo "📡 Watching cron logs..."
# tail -f /var/log/cron.log /var/log/test_cron.log &

# echo "🚀 Starting Flask app..."
# python /app/app.py

#!/bin/bash

# Create log directories and files
mkdir -p /app/logs
touch /app/logs/recommendation_logs.csv /app/logs/click_logs.csv
touch /var/log/cron.log /var/log/test_cron.log /var/log/stock_cron.log

# Start cron
echo "📅 Starting cron..."
cron
pgrep cron || echo "❌ cron did not start"

# Show loaded cron jobs
echo "📋 Loaded cron jobs:"
cat /etc/cron.d/model-cron

# Run initial model training scripts using Conda
echo "🧠 Running model training on container start..."
conda run -n recommender python /app/model.py
conda run -n recommender python /app/stock_model.py  # Optional

# Tail all cron log files
echo "📡 Watching cron logs..."
tail -f /var/log/cron.log /var/log/test_cron.log /var/log/stock_cron.log &

# Start the Flask app using Conda environment
echo "🚀 Starting Flask app..."
conda run -n recommender python /app/app.py
