FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install cron and procps (for pgrep)
RUN apt-get update && apt-get install -y --no-install-recommends cron procps && \
    rm -rf /var/lib/apt/lists/*

# Create log files
RUN touch /var/log/cron.log /var/log/test_cron.log && \
    chmod 666 /var/log/cron.log /var/log/test_cron.log

# Copy cron file first
COPY cronjob /etc/cron.d/model-cron

# Copy app files
COPY . .

# Fix line endings and set up cron
RUN sed -i 's/\r$//' /etc/cron.d/model-cron && \
    echo "" >> /etc/cron.d/model-cron && \
    chmod 0644 /etc/cron.d/model-cron

# Fix start.sh line endings and permissions
COPY start.sh /start.sh
RUN sed -i 's/\r$//' /start.sh && \
    chmod +x /start.sh

EXPOSE 5000

CMD ["/start.sh"]