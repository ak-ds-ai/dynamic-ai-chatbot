# models.py
"""
Database Models for Dynamic AI Chatbot
Includes: Users, Sessions, Messages, Analytics, Feedback, and Intent Training
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Create Base class for all models
Base = declarative_base()


class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User Information
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Session(Base):
    """Session model for tracking conversation sessions"""
    __tablename__ = "sessions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Session Information
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Session Statistics
    total_messages = Column(Integer, default=0)
    avg_sentiment = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.id}, session_id='{self.session_id}', messages={self.total_messages})>"


class Message(Base):
    """Message model for storing all chat messages"""
    __tablename__ = "messages"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    
    # Message Content
    message_text = Column(Text, nullable=False)
    sender = Column(String(10), nullable=False)  # 'user' or 'bot'
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # NLP Features
    intent = Column(String(50), nullable=True, index=True)
    sentiment = Column(String(20), nullable=True, index=True)
    sentiment_score = Column(Float, nullable=True)
    entities = Column(JSON, nullable=True)  # Store extracted entities as JSON
    confidence = Column(Float, nullable=True)
    
    # Performance Metrics
    response_time = Column(Integer, nullable=True)  # in milliseconds
    
    # Additional Metadata
    model_used = Column(String(50), nullable=True)  # e.g., 'gpt-3.5-turbo'
    tokens_used = Column(Integer, nullable=True)
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    feedback_entries = relationship("Feedback", back_populates="message", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Message(id={self.id}, sender='{self.sender}', intent='{self.intent}')>"


class Analytics(Base):
    """Analytics model for storing aggregated session metrics"""
    __tablename__ = "analytics"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    
    # Timestamp
    date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Message Metrics
    total_messages = Column(Integer, default=0)
    user_messages = Column(Integer, default=0)
    bot_messages = Column(Integer, default=0)
    
    # Performance Metrics
    avg_response_time = Column(Float, nullable=True)
    min_response_time = Column(Integer, nullable=True)
    max_response_time = Column(Integer, nullable=True)
    
    # Sentiment Metrics
    positive_sentiment_count = Column(Integer, default=0)
    negative_sentiment_count = Column(Integer, default=0)
    neutral_sentiment_count = Column(Integer, default=0)
    avg_sentiment_score = Column(Float, default=0.0)
    
    # Intent Metrics
    intent_distribution = Column(JSON, nullable=True)  # Store intent stats as JSON
    
    # Engagement Metrics
    avg_message_length = Column(Float, nullable=True)
    conversation_duration = Column(Integer, nullable=True)  # in seconds
    
    # Relationships
    session = relationship("Session", back_populates="analytics")
    
    def __repr__(self):
        return f"<Analytics(id={self.id}, session_id={self.session_id}, messages={self.total_messages})>"


class Feedback(Base):
    """Feedback model for storing user ratings and comments"""
    __tablename__ = "feedback"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False, index=True)
    
    # Feedback Data
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    feedback_type = Column(String(20), nullable=True)  # 'positive', 'negative', 'neutral'
    
    # Categories
    helpful = Column(Boolean, nullable=True)
    accurate = Column(Boolean, nullable=True)
    relevant = Column(Boolean, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="feedback")
    message = relationship("Message", back_populates="feedback_entries")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, rating={self.rating}, message_id={self.message_id})>"


class IntentTraining(Base):
    """Intent Training model for storing training data"""
    __tablename__ = "intent_training"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Training Data
    text = Column(Text, nullable=False)
    intent = Column(String(50), nullable=False, index=True)
    
    # Validation
    is_validated = Column(Boolean, default=False)
    validated_by = Column(String(50), nullable=True)
    
    # Metadata
    source = Column(String(50), nullable=True)  # 'manual', 'automatic', 'imported'
    confidence = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<IntentTraining(id={self.id}, intent='{self.intent}', validated={self.is_validated})>"


class ErrorLog(Base):
    """Error Log model for tracking system errors"""
    __tablename__ = "error_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Error Information
    error_type = Column(String(100), nullable=False, index=True)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    
    # Context
    endpoint = Column(String(100), nullable=True)
    user_input = Column(Text, nullable=True)
    session_id = Column(String(100), nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Status
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<ErrorLog(id={self.id}, type='{self.error_type}', resolved={self.is_resolved})>"


# Helper function to create all tables
def create_all_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)
    print("✓ All database tables created successfully!")


# Helper function to drop all tables (use with caution!)
def drop_all_tables(engine):
    """Drop all tables from the database"""
    Base.metadata.drop_all(bind=engine)
    print("✓ All database tables dropped!")


if __name__ == "__main__":
    # Test the models
    print("=" * 60)
    print("Database Models Test")
    print("=" * 60)
    
    # List all models
    models = [
        User, Session, Message, Analytics, 
        Feedback, IntentTraining, ErrorLog
    ]
    
    print("\nDefined Models:")
    for model in models:
        print(f"  ✓ {model.__name__}: {model.__tablename__}")
    
    print("\nRelationships:")
    print("  ✓ User → Sessions (one-to-many)")
    print("  ✓ User → Feedback (one-to-many)")
    print("  ✓ Session → Messages (one-to-many)")
    print("  ✓ Session → Analytics (one-to-many)")
    print("  ✓ Message → Feedback (one-to-many)")
    
    print("\n" + "=" * 60)
    print("Models defined successfully!")
    print("Run 'python database.py' to create tables")
    print("=" * 60)