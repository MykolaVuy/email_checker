import os

# Base directory — from where the script is run (e.g. via cron or manually)
BASE_DIR = os.getcwd()

# Config files (disposable_domains.json) remain inside the package
CONFIG_DIR = os.path.join(os.path.dirname(__file__))

# Path to files to process — input folder in BASE_DIR
INPUT_DIR = os.path.join(BASE_DIR, "input")

# Path to the list of disposable email domains
DISPOSABLE_DOMAINS_FILE = os.path.join(CONFIG_DIR, "data", "disposable_domains.json")

# Limit on the number of emails per 1 launch
MAX_EMAILS_PER_RUN = 50

# Test sender for SMTP verification
SMTP_FROM = "verify@example.com"

# Timeout for SMTP requests
SMTP_TIMEOUT = 10

# URL for updating the list of disposable email domains
DISPOSABLE_DOMAINS_URL = "https://raw.githubusercontent.com/Propaganistas/Laravel-Disposable-Email/master/domains.json"

# Logging into the terminal
DEBUG = True
