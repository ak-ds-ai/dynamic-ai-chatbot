# test_integration.py
"""
Integration test for NLP Service + OpenAI Service
"""

from nlp_service import NLPService
from openai_service import OpenAIService


def test_integration():
    print("=" * 60)
    print("NLP + OpenAI Integration Test")
    print("=" * 60)
    
    # Initialize services
    print("\nInitializing services...")
    nlp = NLPService()
    ai = OpenAIService()
    
    # Test messages
    test_cases = [
        {
            'message': "Hello! I need help booking a flight",
            'description': "Greeting + Help + Booking"
        },
        {
            'message': "This is terrible! Nothing is working!",
            'description': "Negative Complaint"
        },
        {
            'message': "Can you schedule a meeting for tomorrow at 2pm? My email is john@example.com",
            'description': "Question with Entities"
        },
        {
            'message': "Thank you so much for your help!",
            'description': "Positive Thanks"
        }
    ]
    
    print("\n" + "=" * 60)
    print("Processing Test Messages")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        message = test_case['message']
        description = test_case['description']
        
        print(f"\n{i}. {description}")
        print("-" * 60)
        print(f"User: {message}")
        
        # Step 1: NLP Processing
        nlp_result = nlp.process_message(message)
        print(f"\nNLP Analysis:")
        print(f"  Intent: {nlp_result['intent']} ({nlp_result['confidence']:.2f})")
        print(f"  Sentiment: {nlp_result['sentiment']} ({nlp_result['sentiment_score']:.2f})")
        
        # FIXED: Handle entities printing properly
        if nlp_result['entities']:
            entities_list = [f"{e['type']}:{e['text']}" for e in nlp_result['entities']]
            entities_str = ', '.join(entities_list)
            print(f"  Entities: {entities_str}")
        
        # Step 2: AI Response Generation
        ai_result = ai.generate_response_sync(
            user_message=message,
            intent=nlp_result['intent'],
            sentiment=nlp_result['sentiment'],
            entities=nlp_result['entities']
        )
        
        if ai_result['success']:
            print(f"\nAI Response:")
            print(f"  {ai_result['response']}")
            print(f"  Time: {ai_result['response_time']}ms")
            print(f"  Tokens: {ai_result.get('tokens_used', 'N/A')}")
        else:
            print(f"\n✗ AI Error: {ai_result.get('error')}")
    
    print("\n" + "=" * 60)
    print("✓ Integration test complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()