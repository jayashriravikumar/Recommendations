# FROM python:3.11-slim


# # Install system dependencies
# RUN apt-get update && apt-get install -y libgomp1

# WORKDIR /app

# # Install dependencies first for caching
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Install cron and procps (for pgrep)
# RUN apt-get update && apt-get install -y --no-install-recommends cron procps && \
#     rm -rf /var/lib/apt/lists/*

# # Create log files
# RUN touch /var/log/cron.log /var/log/test_cron.log /var/log/stock_cron.log && \
#     chmod 666 /var/log/cron.log /var/log/test_cron.log /var/log/stock_cron.log

# # Copy cron file first
# COPY cronjob /etc/cron.d/model-cron

# # Copy app files
# COPY . .
# RUN python3 model.py
# RUN python3 stock_model.py

# # Fix line endings and set up cron
# RUN sed -i 's/\r$//' /etc/cron.d/model-cron && \
#     echo "" >> /etc/cron.d/model-cron && \
#     chmod 0644 /etc/cron.d/model-cron

# # Fix start.sh line endings and permissions
# COPY start.sh /start.sh
# RUN sed -i 's/\r$//' /start.sh && \
#     chmod +x /start.sh

# EXPOSE 5000

# CMD ["/start.sh"]

# Base image with CUDA runtime support
FROM nvidia/cuda:12.1.1-runtime-ubuntu20.04

# Install system tools and dependencies
RUN apt-get update && apt-get install -y \
    curl git build-essential cron procps libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV CONDA_AUTO_UPDATE_CONDA=false
ENV PATH /opt/conda/bin:$PATH
RUN curl -o miniconda.sh -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Create environment and install faiss-gpu + Python deps
# RUN conda create -n recommender python=3.10 -y && \
#     /opt/conda/bin/conda run -n recommender conda install -c conda-forge faiss-gpu -y && \
#     /opt/conda/bin/conda run -n recommender conda install -c conda-forge pandas flask lightgbm scikit-learn -y
RUN conda create -n recommender python=3.10 -y

# Install faiss-gpu separately (big download)
RUN /opt/conda/bin/conda run -n recommender conda install -c conda-forge faiss-gpu -y

# Install the rest of your packages
RUN /opt/conda/bin/conda run -n recommender conda install --override-channels -c conda-forge pandas flask flask-cors lightgbm scikit-learn -y


# Set working directory
WORKDIR /app

# Copy requirements before code (optional if using pip)
COPY requirements.txt .

# Copy cronjob file before using sed/chmod
COPY cronjob /etc/cron.d/model-cron

# Fix line endings for cronjob
RUN sed -i 's/\r$//' /etc/cron.d/model-cron && chmod 0644 /etc/cron.d/model-cron

# Copy codebase
COPY . .

# Set environment to activate the conda env in scripts
ENV PATH /opt/conda/envs/recommender/bin:$PATH

# Copy start.sh explicitly
COPY start.sh /start.sh

# Fix line endings for start.sh
RUN sed -i 's/\r$//' /start.sh && chmod +x /start.sh

# Pre-run model training
RUN conda run -n recommender python /app/model.py && \
    conda run -n recommender python /app/stock_model.py

# Expose Flask port
EXPOSE 5000

# Default command
CMD ["/start.sh"]
