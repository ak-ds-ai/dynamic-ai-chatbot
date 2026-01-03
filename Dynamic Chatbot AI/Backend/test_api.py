# test_api.py
"""Test the FastAPI endpoints"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    print("\n1. Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health():
    print("\n2. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_chat():
    print("\n3. Testing Chat Endpoint...")
    data = {
        "session_id": "test_session_123",
        "message": "Hello! I need help booking a flight to New York tomorrow"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result['response']}")
    print(f"Intent: {result['intent']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Entities: {result['entities']}")
    print(f"Response Time: {result['response_time']}ms")

def test_analytics():
    print("\n4. Testing Analytics...")
    response = requests.get(f"{BASE_URL}/api/analytics/test_session_123")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_history():
    print("\n5. Testing History...")
    response = requests.get(f"{BASE_URL}/api/history/test_session_123")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total Messages: {data['total_messages']}")
    for msg in data['messages']:
        print(f"  [{msg['sender']}]: {msg['text'][:50]}...")

if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI Endpoint Tests")
    print("=" * 60)
    
    try:
        test_root()
        test_health()
        test_chat()
        test_analytics()
        test_history()
        
        print("\n" + "=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to API")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")