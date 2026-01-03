# test_env.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("Environment Variables Test")
print("=" * 60)

# Test all environment variables
env_vars = {
    "DATABASE_URL": os.getenv("postgresql://chatbot_user:Somnath@2004@localhost:5432/chatbot_db"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "APP_HOST": os.getenv("APP_HOST"),
    "APP_PORT": os.getenv("APP_PORT"),
    "DEBUG": os.getenv("DEBUG"),
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS"),
    "REDIS_URL": os.getenv("REDIS_URL"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL")
}

# Check each variable
all_ok = True
for key, value in env_vars.items():
    if value:
        # Mask sensitive information
        if key in ["DATABASE_URL", "OPENAI_API_KEY", "SECRET_KEY"]:
            masked_value = value[:15] + "..." if len(value) > 15 else "***"
            print(f"✓ {key}: {masked_value}")
        else:
            print(f"✓ {key}: {value}")
    else:
        print(f"✗ {key}: NOT SET")
        all_ok = False

print("=" * 60)

if all_ok:
    print("✓ All environment variables are configured!")
    
    # Test database connection
    print("\nTesting database connection...")
    try:
        import psycopg2
        db_url = os.getenv("DATABASE_URL")
        
        # Parse DATABASE_URL
        # Format: postgresql://user:password@host:port/database
        from urllib.parse import urlparse
        result = urlparse(db_url)
        
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        print("✓ Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
    
    # Check if OpenAI API key format is correct
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        print("✓ OpenAI API key format looks correct")
    else:
        print("⚠ OpenAI API key format might be incorrect (should start with 'sk-')")
    
else:
    print("✗ Some environment variables are missing!")
    print("\nPlease check your .env file and ensure all variables are set.")

print("=" * 60)