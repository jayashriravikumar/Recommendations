#!/bin/bash

echo "📅 Starting cron..."
cron
pgrep cron || echo "❌ cron did not start"

touch /var/log/cron.log /var/log/test_cron.log
echo "📋 Loaded cron jobs:"
cat /etc/cron.d/model-cron

echo "📡 Watching cron logs..."
tail -f /var/log/cron.log /var/log/test_cron.log &

echo "🚀 Starting Flask app..."
python /app/app.py