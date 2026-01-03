# test_nlp.py
from nlp_service import NLPService

def test_nlp():
    print("Testing NLP Service Components\n")
    
    nlp = NLPService()
    
    # Test 1: Intent Recognition
    print("1. INTENT RECOGNITION TEST")
    print("-" * 50)
    test_intents = [
        ("Hello there!", "greeting"),
        ("I need help", "help"),
        ("Goodbye", "farewell"),
        ("Book a table", "booking"),
        ("This is broken", "complaint"),
        ("Thank you", "thanks")
    ]
    
    for text, expected in test_intents:
        intent, conf = nlp.recognize_intent(text)
        status = "✓" if intent == expected else "✗"
        print(f"{status} '{text}' → {intent} (expected: {expected})")
    
    # Test 2: Sentiment Analysis
    print("\n2. SENTIMENT ANALYSIS TEST")
    print("-" * 50)
    test_sentiments = [
        ("I love this product!", "positive"),
        ("This is terrible", "negative"),
        ("The weather is okay", "neutral")
    ]
    
    for text, expected in test_sentiments:
        sentiment, score = nlp.analyze_sentiment(text)
        status = "✓" if sentiment == expected else "✗"
        print(f"{status} '{text}' → {sentiment} ({score:.2f})")
    
    # Test 3: Entity Extraction
    print("\n3. ENTITY EXTRACTION TEST")
    print("-" * 50)
    test_entities = [
        "My email is test@example.com",
        "Call me at 123-456-7890",
        "Meeting tomorrow at 3pm",
        "The cost is $99.99"
    ]
    
    for text in test_entities:
        entities = nlp.extract_entities(text)
        print(f"'{text}'")
        for ent in entities:
            print(f"   → {ent['type']}: {ent['text']}")
    
    print("\n" + "=" * 50)
    print("✓ All tests complete!")

if __name__ == "__main__":
    test_nlp()