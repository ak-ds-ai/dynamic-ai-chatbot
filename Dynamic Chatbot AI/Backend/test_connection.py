import psycopg2

try:
    conn = psycopg2.connect(
        dbname="chatbot_db",
        user="chatbot_user",
        password="Somnath@2004",
        host="localhost",
        port="5432"
    )
    print("✓ Database connection successful!")
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"✓ PostgreSQL version: {version[0]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Connection failed: {e}")