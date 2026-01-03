# openai_service.py - PURE MOCK - NO EXTERNAL DEPENDENCIES
from typing import List, Dict
import time
import random

class OpenAIService:
    def __init__(self):
        print("Initializing OpenAI Service...")
        print("✓ OpenAI Service initialized")
        print("  Model: gpt-3.5-turbo")
        print("  Max Tokens: 500")
        print("  Temperature: 0.7")
        print("  🎭 MOCK MODE ACTIVE - NO API - NO COSTS")
    
    def build_system_prompt(self, sentiment, intent, entities):
        return "mock"
    
    def generate_response_sync(self, user_message, context=None, sentiment='neutral', intent='general', entities=None):
        context = context or []
        entities = entities or []
        start = time.time()
        
        responses = {
            'greeting': "Hello! How can I help you today?",
            'farewell': "Goodbye! Have a great day!",
            'question': "That's a great question! Let me help with that.",
            'help': "I'm here to help! What do you need?",
            'booking': "I can help you with that booking.",
            'complaint': "I'm sorry about this issue. Let me help fix it.",
            'thanks': "You're welcome! Happy to help!",
            'denial': "No problem! Anything else I can do?",
            'general': "I understand. How can I assist you?"
        }
        
        response = responses.get(intent, responses['general'])
        
        if sentiment == 'negative':
            response = "I understand your frustration. " + response
        
        time.sleep(0.4)
        return {
            'success': True,
            'response': response,
            'response_time': int((time.time() - start) * 1000),
            'tokens_used': random.randint(80, 150),
            'model': 'mock-gpt-3.5-turbo'
        }
    
    async def generate_response(self, user_message, context, sentiment='neutral', intent='general', entities=None):
        return self.generate_response_sync(user_message, context, sentiment, intent, entities)