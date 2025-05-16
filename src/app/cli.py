import sys
from app.services.checker import check_email

def run_cli():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("⚠️  Usage: python cli.py email@example.com [-S | short | -F | full]")
        sys.exit(1)

    email = sys.argv[1]
    verbosity = None

    if len(sys.argv) == 3:
        arg = sys.argv[2].lower()
        if arg in ("-s", "short"):
            verbosity = "short"
        elif arg in ("-f", "full"):
            verbosity = "full"
        else:
            print(f"⚠️  Unknown verbosity option: {arg}")
            sys.exit(1)

    result = check_email(email, verbosity)
    print(f"{email} → {result}")

if __name__ == "__main__":
    run_cli()
