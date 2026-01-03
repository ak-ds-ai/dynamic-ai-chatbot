# test_models.py
from sqlalchemy.orm import Session as DBSession
from database import SessionLocal
from models import User, Session, Message, Analytics, Feedback
import json

def test_all():
    print("=" * 60)
    print("Testing Database Models")
    print("=" * 60)
    
    db: DBSession = SessionLocal()
    
    try:
        # Create test user
        print("\n1. Creating user...")
        user = User(
            username="john_doe",
            email="john@example.com",
            full_name="John Doe"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"   ✓ User: {user.username} (ID: {user.id})")
        
        # Create session
        print("\n2. Creating session...")
        session = Session(
            session_id="session_001",
            user_id=user.id
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        print(f"   ✓ Session: {session.session_id}")
        
        # Create messages
        print("\n3. Creating messages...")
        msg1 = Message(
            session_id=session.id,
            message_text="Hello!",
            sender="user",
            intent="greeting",
            sentiment="positive",
            entities=json.dumps([{"type": "GREETING", "value": "Hello"}])
        )
        msg2 = Message(
            session_id=session.id,
            message_text="Hi! How can I help?",
            sender="bot",
            intent="greeting",
            sentiment="positive",
            response_time=150
        )
        db.add(msg1)
        db.add(msg2)
        db.commit()
        print(f"   ✓ Messages: 2 created")
        
        # Update session
        print("\n4. Updating session...")
        session.total_messages = 2
        db.commit()
        print(f"   ✓ Session updated: {session.total_messages} messages")
        
        # Create analytics
        print("\n5. Creating analytics...")
        analytics = Analytics(
            session_id=session.id,
            total_messages=2,
            user_messages=1,
            bot_messages=1,
            avg_response_time=150.0
        )
        db.add(analytics)
        db.commit()
        print(f"   ✓ Analytics created")
        
        # Query data
        print("\n6. Querying data...")
        users_count = db.query(User).count()
        sessions_count = db.query(Session).count()
        messages_count = db.query(Message).count()
        print(f"   ✓ Users: {users_count}")
        print(f"   ✓ Sessions: {sessions_count}")
        print(f"   ✓ Messages: {messages_count}")
        
        # Test relationships
        print("\n7. Testing relationships...")
        user_sessions = user.sessions
        session_messages = session.messages
        print(f"   ✓ User has {len(user_sessions)} session(s)")
        print(f"   ✓ Session has {len(session_messages)} message(s)")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
        # Cleanup
        cleanup = input("\nDelete test data? (y/n): ")
        if cleanup.lower() == 'y':
            db.delete(analytics)
            db.delete(msg2)
            db.delete(msg1)
            db.delete(session)
            db.delete(user)
            db.commit()
            print("✓ Cleaned up!")
        else:
            print("Data kept in database.")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_all()