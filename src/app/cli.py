import sys
from app.services.checker import check_email

def run_cli():
    if len(sys.argv) != 2:
        print("⚠️  Usage: python cli.py email@example.com")
        sys.exit(1)

    email = sys.argv[1]
    result = check_email(email)
    print(f"{email} → {result}")

if __name__ == "__main__":
    run_cli()
