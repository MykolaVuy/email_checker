import os
import importlib.util

# Base directory — from where the script is run (e.g. via cron or manually)
BASE_DIR = os.getcwd()

# Config files (disposable_domains.json) remain inside the package
CONFIG_DIR = os.path.join(os.path.dirname(__file__))

# Path to files to process — input folder in BASE_DIR
INPUT_DIR = os.path.join(BASE_DIR, "input")

# Path to the list of disposable email domains
DISPOSABLE_DOMAINS_FILE = os.path.join(CONFIG_DIR, "data", "disposable_domains.json")

# URL for updating the list of disposable email domains
DISPOSABLE_DOMAINS_URL = "https://raw.githubusercontent.com/Propaganistas/Laravel-Disposable-Email/master/domains.json"

# Optional values (can be overridden)

# Limit on the number of emails per 1 launch
MAX_EMAILS_PER_RUN = 50

# Test sender for SMTP verification
SMTP_FROM = "verify@example.com"

# Timeout for SMTP requests
SMTP_TIMEOUT = 10

# SMTP EHLO/HELO settings
USE_EHLO = False

# Domain for EHLO/HELO command
EHLO_DOMAIN = ""

# Use a random email address for the FROM field
USE_RANDOM_FROM = False

# Custom domain for the random FROM email address
CUSTOM_FROM_DOMAIN = ""

# Logging into the terminal
DEBUG = True

# User config path (project-local)
USER_CONFIG_PATH = os.path.join(BASE_DIR, "email_checker_user_config.py")

# Try to load user config
if os.path.exists(USER_CONFIG_PATH):
    spec = importlib.util.spec_from_file_location("user_config", USER_CONFIG_PATH)
    user_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_config)

    for key in dir(user_config):
        if key.isupper():
            globals()[key] = getattr(user_config, key)
