# nlp_service.py
"""
NLP Service for Dynamic AI Chatbot
Handles: Intent Recognition, Sentiment Analysis, Named Entity Recognition
"""

import spacy
from textblob import TextBlob
import re
from typing import List, Dict, Tuple
import json

class NLPService:
    """
    NLP Service for processing user messages
    Features:
    - Intent Recognition
    - Sentiment Analysis
    - Named Entity Recognition (NER)
    """
    
    def __init__(self):
        """Initialize NLP models and patterns"""
        print("Initializing NLP Service...")
        
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model loaded")
        except Exception as e:
            print(f"⚠ spaCy model not loaded: {e}")
            print("  Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Intent patterns with keywords
        self.intent_patterns = {
            'greeting': {
                'keywords': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 
                           'good evening', 'greetings', 'howdy', 'hiya'],
                'weight': 1.0
            },
            'farewell': {
                'keywords': ['bye', 'goodbye', 'see you', 'later', 'farewell', 
                           'take care', 'catch you later', 'bye bye'],
                'weight': 1.0
            },
            'question': {
                'keywords': ['what', 'when', 'where', 'who', 'why', 'how', 'which',
                           'can you', 'could you', 'would you', '?'],
                'weight': 0.8
            },
            'help': {
                'keywords': ['help', 'assist', 'support', 'guide', 'instructions',
                           'how to', 'need help', 'can you help'],
                'weight': 1.0
            },
            'booking': {
                'keywords': ['book', 'reserve', 'appointment', 'schedule', 'meeting',
                           'reservation', 'booking'],
                'weight': 1.0
            },
            'complaint': {
                'keywords': ['complaint', 'issue', 'problem', 'not working', 'broken',
                           'error', 'wrong', 'bad', 'terrible', 'awful'],
                'weight': 0.9
            },
            'thanks': {
                'keywords': ['thank', 'thanks', 'appreciate', 'grateful', 'thx',
                           'thank you', 'thanks a lot'],
                'weight': 1.0
            },
            'information': {
                'keywords': ['tell me', 'show me', 'explain', 'describe', 'information',
                           'details', 'about', 'what is'],
                'weight': 0.7
            },
            'confirmation': {
                'keywords': ['yes', 'yeah', 'sure', 'okay', 'ok', 'alright', 'correct',
                           'right', 'definitely', 'absolutely'],
                'weight': 0.9
            },
            'denial': {
                'keywords': ['no', 'nope', 'not', 'never', 'incorrect', 'wrong',
                           'negative', 'nah'],
                'weight': 0.9
            }
        }
        
        print("✓ NLP Service initialized successfully")
    
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities from text using spaCy and regex patterns
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of dictionaries containing entity information
        """
        entities = []
        
        # Use spaCy NER if available
        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    entities.append({
                        'text': ent.text,
                        'type': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char
                    })
            except Exception as e:
                print(f"spaCy NER error: {e}")
        
        # Additional regex-based entity extraction
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entities.append({
                'text': match.group(),
                'type': 'EMAIL',
                'start': match.start(),
                'end': match.end()
            })
        
        # Phone number extraction
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format: 123-456-7890
            r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',  # (123) 456-7890
            r'\b\+\d{1,3}\s*\d{1,4}\s*\d{1,4}\s*\d{1,9}\b'  # International
        ]
        for pattern in phone_patterns:
            for match in re.finditer(pattern, text):
                entities.append({
                    'text': match.group(),
                    'type': 'PHONE',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Date extraction
        date_patterns = [
            r'\b(today|tomorrow|yesterday)\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(st|nd|rd|th)?\b'
        ]
        for pattern in date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(),
                    'type': 'DATE',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Time extraction
        time_patterns = [
            r'\b\d{1,2}:\d{2}\s*(am|pm|AM|PM)?\b',
            r'\b(morning|afternoon|evening|night)\b'
        ]
        for pattern in time_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(),
                    'type': 'TIME',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Money extraction
        money_patterns = [
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
            r'\b\d+\s*(?:dollars?|USD|EUR|rupees?|INR)\b'
        ]
        for pattern in money_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(),
                    'type': 'MONEY',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # URL extraction
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        for match in re.finditer(url_pattern, text):
            entities.append({
                'text': match.group(),
                'type': 'URL',
                'start': match.start(),
                'end': match.end()
            })
        
        return entities
    
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text using TextBlob
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (sentiment_label, polarity_score)
            - sentiment_label: 'positive', 'negative', or 'neutral'
            - polarity_score: Float between -1 (negative) and 1 (positive)
        """
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Classify sentiment based on polarity
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return sentiment, polarity
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 'neutral', 0.0
    
    
    def recognize_intent(self, text: str) -> Tuple[str, float]:
        """
        Recognize user intent from text using keyword matching
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (intent, confidence_score)
            - intent: Detected intent (e.g., 'greeting', 'question', 'booking')
            - confidence_score: Float between 0 and 1
        """
        text_lower = text.lower()
        intent_scores = {}
        
        # Calculate score for each intent
        for intent, data in self.intent_patterns.items():
            score = 0
            keywords = data['keywords']
            weight = data['weight']
            
            # Count matching keywords
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            # Apply weight and normalize
            if score > 0:
                intent_scores[intent] = (score / len(keywords)) * weight
        
        # Get intent with highest score
        if intent_scores:
            detected_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[detected_intent], 1.0)
            return detected_intent, confidence
        
        # Default to 'general' if no intent detected
        return 'general', 0.5
    
    
    def process_message(self, text: str) -> Dict:
        """
        Process a message with all NLP features
        
        Args:
            text: Input message text
            
        Returns:
            Dictionary containing all NLP analysis results
        """
        # Extract entities
        entities = self.extract_entities(text)
        
        # Analyze sentiment
        sentiment, sentiment_score = self.analyze_sentiment(text)
        
        # Recognize intent
        intent, confidence = self.recognize_intent(text)
        
        # Compile results
        result = {
            'original_text': text,
            'intent': intent,
            'confidence': confidence,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'entities': entities,
            'entity_count': len(entities)
        }
        
        return result


# Test the NLP Service
if __name__ == "__main__":
    print("=" * 60)
    print("NLP Service Test")
    print("=" * 60)
    
    # Initialize service
    nlp_service = NLPService()
    
    # Test messages
    test_messages = [
        "Hello! How are you today?",
        "I need to book an appointment for tomorrow at 3pm",
        "This product is terrible and not working!",
        "Can you help me with my account? My email is john@example.com",
        "Thank you so much for your assistance!",
        "What is the weather like today?",
        "I want to schedule a meeting on Monday morning",
        "The price is $299.99 for this service"
    ]
    
    print("\nTesting NLP processing...\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Message: \"{message}\"")
        print("-" * 60)
        
        result = nlp_service.process_message(message)
        
        print(f"   Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        print(f"   Sentiment: {result['sentiment']} (score: {result['sentiment_score']:.2f})")
        
        if result['entities']:
            print(f"   Entities found: {result['entity_count']}")
            for entity in result['entities']:
                print(f"      - {entity['type']}: {entity['text']}")
        else:
            print("   Entities: None detected")
    
    print("\n" + "=" * 60)
    print("✓ NLP Service test complete!")
    print("=" * 60)