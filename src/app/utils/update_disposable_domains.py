import requests
import json
import os

from app.config import DISPOSABLE_DOMAINS_FILE, DISPOSABLE_DOMAINS_URL

def update_domains():
    try:
        response = requests.get(DISPOSABLE_DOMAINS_URL)
        response.raise_for_status()

        domains = response.json()
        os.makedirs(os.path.dirname(DISPOSABLE_DOMAINS_FILE), exist_ok=True)

        with open(DISPOSABLE_DOMAINS_FILE, "w") as f:
            json.dump(domains, f, indent=2)

        print(f"✅ Disposable domains updated, total: {len(domains)}")
    except Exception as e:
        print(f"❌ Failed to update disposable domains: {e}")

if __name__ == "__main__":
    update_domains()
