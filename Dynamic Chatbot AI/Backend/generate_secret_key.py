# generate_secret_key.py
import secrets

def generate_secret_key():
    """Generate a secure random secret key"""
    secret_key = secrets.token_urlsafe(32)
    print("Your secure secret key:")
    print(secret_key)
    print("\nCopy this and paste it in your .env file:")
    print(f"SECRET_KEY={secret_key}")

if __name__ == "__main__":
    generate_secret_key()