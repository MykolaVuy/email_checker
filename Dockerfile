FROM python:3.12-slim

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    wget \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy files
COPY . .

# Add PYTHONPATH
ENV PYTHONPATH=/app/src

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install the package from pyproject.toml
RUN pip install .

# Install the disposable email domains
RUN mkdir -p src/app/data && \
    wget -q https://raw.githubusercontent.com/Propaganistas/Laravel-Disposable-Email/master/domains.json -O src/app/data/disposable_domains.json

# Create cron jobs
RUN echo "*/30 * * * * cd /app && /usr/local/bin/check_batch >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron
RUN echo "0 3 * * 1 cd /app && /usr/local/bin/python3 src/app/utils/update_disposable_domains.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/app-cron

# Set permissions for the cron file
RUN chmod 0644 /etc/cron.d/app-cron

# Add cron to the system
RUN crontab /etc/cron.d/app-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Launch cron and tail the log file
CMD cron && tail -f /var/log/cron.log
