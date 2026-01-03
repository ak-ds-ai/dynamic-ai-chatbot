# FREE Backend - No OpenAI API Key Required!
# This is an AI that answers questions locally
from email.mime import message
import subprocess
from database import engine
from models import Base
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies import get_current_user
from database import get_db
from models import User
from auth import hash_password

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
from auth import verify_password
from jwt_utils import create_access_token
   
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


Base.metadata.create_all(bind=engine)
# -------- LLM INTERFACE (OLLAMA) --------
OLLAMA_PATH = r"C:\Users\akash\AppData\Local\Programs\Ollama\ollama.exe"

def generate_llm_response(prompt: str) -> str:
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", "llama3:8b"],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120
        )

        if result.stdout.strip():
            return result.stdout.strip()

        if result.stderr.strip():
            return f"⚠️ Ollama error: {result.stderr.strip()}"

        return "⚠️ LLM returned no output."

    except Exception as e:
        return f"⚠️ Exception calling Ollama: {str(e)}"


# -------- PROMPT BUILDER --------

def build_prompt(history, user_message):
    conversation = ""
    for msg in history[-6:]:
        conversation += f"{msg['role'].capitalize()}: {msg['content']}\n"

    prompt = f"""
You are a helpful, conversational AI assistant.
Answer clearly and naturally.

Conversation so far:
{conversation}

User: {user_message}
Assistant:
"""
    return prompt

# ----------FastAPI Backend--------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import re

app = FastAPI()
@app.post("/api/login")
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    # 1. Find user by email
    user = db.query(User).filter(User.email == request.email).first()

    # 2. Check email & password
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 3. Create JWT token
    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/api/register")
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    # 1. Check if user already exists
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2. Hash password
    hashed_pw = hash_password(request.password)

    # 3. Create user
    new_user = User(
        email=request.email,
        hashed_password=hashed_pw
    )

    # 4. Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: str
    sentiment: str
    entities: list
    response_time: int
# ------------------------------
# SESSION MEMORY (IN-MEMORY)
# ------------------------------
SESSION_MEMORY = {}

def get_session_history(session_id: str):
    return SESSION_MEMORY.get(session_id, [])

def save_to_memory(session_id: str, role: str, content: str):
    SESSION_MEMORY.setdefault(session_id, []).append({
        "role": role,
        "content": content
    })


# Knowledge Base - Add more Q&A here!
KNOWLEDGE_BASE = {
    "machine learning": """Machine Learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. 

Key concepts:
• Supervised Learning - Learning from labeled data
• Unsupervised Learning - Finding patterns in unlabeled data
• Neural Networks - Inspired by the human brain
• Deep Learning - Multiple layers of neural networks

Applications include image recognition, natural language processing, recommendation systems, and autonomous vehicles.""",

    "deep learning": """Deep Learning is a subset of machine learning that uses artificial neural networks with multiple layers (hence "deep") to progressively extract higher-level features from raw input.

Key features:
• Uses neural networks with many layers
• Automatically learns feature representations
• Excels at tasks like image recognition, speech recognition, and NLP
• Requires large amounts of data and computational power

Popular frameworks: TensorFlow, PyTorch, Keras""",

    "neural network": """A Neural Network is a computing system inspired by biological neural networks in animal brains. It consists of interconnected nodes (neurons) organized in layers.

Structure:
• Input Layer - Receives data
• Hidden Layers - Process information
• Output Layer - Produces results

Types: Feedforward, Convolutional (CNN), Recurrent (RNN), Transformer""",

    "nlp": """Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and manipulate human language.

Key tasks:
• Text Classification
• Sentiment Analysis
• Named Entity Recognition (NER)
• Machine Translation
• Question Answering
• Text Summarization

Popular models: BERT, GPT, T5, RoBERTa""",

    "python": """Python is a high-level, interpreted programming language known for its simplicity and readability. It's extremely popular for:

• Data Science & Machine Learning
• Web Development
• Automation & Scripting
• Scientific Computing

Key libraries: NumPy, Pandas, TensorFlow, PyTorch, Scikit-learn, Django, Flask""",

    "ai": """Artificial Intelligence (AI) is the simulation of human intelligence by machines. It includes:

• Machine Learning - Learning from data
• Deep Learning - Neural networks
• Natural Language Processing - Understanding text
• Computer Vision - Understanding images
• Robotics - Physical AI systems

AI is transforming industries from healthcare to finance to transportation.""",

    "data science": """Data Science is an interdisciplinary field that uses scientific methods, processes, and algorithms to extract knowledge and insights from structured and unstructured data.

Key skills:
• Statistics & Mathematics
• Programming (Python, R)
• Data Visualization
• Machine Learning
• Domain Knowledge

Career paths: Data Scientist, ML Engineer, Data Analyst, AI Researcher""",

    "chatgpt": """ChatGPT is a large language model developed by OpenAI based on the GPT (Generative Pre-trained Transformer) architecture.

Features:
• Understands and generates human-like text
• Can answer questions, write code, create content
• Trained on vast amounts of internet text
• Uses transformer architecture
• Supports conversational interactions

You're talking to a chatbot inspired by ChatGPT right now!"""
}

def get_ai_response(message: str, session_id: str) -> str:
    history = get_session_history(session_id)

    def prefers_short_answers():
        return any(
            entry["role"] == "system" and entry["content"] == "pref:short_answers"
            for entry in reversed(history)
    )

    message_lower = message.lower().strip()


    # -------- NAME MEMORY LOGIC --------
    if message_lower.startswith("my name is"):
        name = message.split("my name is")[-1].strip().title()
        save_to_memory(session_id, "system", f"name:{name}")
        return f"Nice to meet you, {name}! I’ll remember your name 😊"
    elif "what is my name" in message_lower or "do you know my name" in message_lower:
        for entry in reversed(history):
            if entry["role"] == "system" and entry["content"].startswith("name:"):
                name = entry["content"].split("name:")[-1]
                return f"Your name is {name}! 😊"
        return "I don't know your name yet. You can tell me by saying 'My name is ...'."

# -------- USER FACT MEMORY --------
    fact_patterns = [
    "i like ",
    "i love ",
    "i am learning ",
    "i'm learning ",
    "i prefer ",
    "i want ",
    "my goal is ",
    "i am a ",
    "i'm a "
]

    for pattern in fact_patterns:
        if message_lower.startswith(pattern):
            fact = message[len(pattern):].strip()
            save_to_memory(session_id, "system", f"fact:{pattern}{fact}")
            return "Got it 👍 I’ll remember that."
        

# -------- PREFERENCE: SHORT ANSWERS --------
    if message_lower.startswith("i prefer short"):
        save_to_memory(session_id, "system", "pref:short_answers")
        return "Got it 👍 I’ll keep explanations short."
    

# -------- FACT RECALL --------
    if "what do you know about me" in message_lower:
        facts = [
            entry["content"].replace("fact:", "")
            for entry in reversed(history)
            if entry["role"] == "system" and entry["content"].startswith("fact:")
    ]

        if facts:
            return "Here’s what I remember about you:\n- " + "\n- ".join(facts)

        return "I don’t have any personal details about you yet."


    # Check knowledge base for matches
    for topic, response in KNOWLEDGE_BASE.items():
        if topic in message_lower:
            if prefers_short_answers():
            # Short explanation (first 1–2 lines)
                short = response.split("\n")[0]
                return short
            return response

    
    # Greeting responses
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm here to help you learn about AI, Machine Learning, Deep Learning, and related topics. What would you like to know?"
    
    # Gratitude responses
    if any(word in message_lower for word in ["thank", "thanks"]):
        return "You're welcome! Feel free to ask me anything about AI, ML, Deep Learning, NLP, Data Science, or programming!"
    
    # Help requests
    if any(word in message_lower for word in ["help", "assist"]):
        return """I can help you with:
• Machine Learning concepts
• Deep Learning & Neural Networks
• Natural Language Processing (NLP)
• Python programming
• Data Science
• Artificial Intelligence
• ChatGPT and LLMs

Just ask me a question about any of these topics!"""
    
    # Question about capabilities
    if "what can you do" in message_lower or "your capabilities" in message_lower:
        return """I can:
✓ Answer questions about AI, ML, and Deep Learning
✓ Explain programming concepts (especially Python)
✓ Discuss data science topics
✓ Provide information about NLP and neural networks
✓ Help you understand ChatGPT and LLMs
✓ Detect sentiment and intent in your messages
✓ Extract entities like emails and dates

Try asking me about any of these topics!"""
    prompt = build_prompt(history,message)
    return generate_llm_response(prompt)
 

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "timestamp": datetime.now().isoformat(),
        "message": "Backend running - No API key required!"
    }

@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Protected chat endpoint – requires JWT
    """
    start_time = datetime.now()

    response_text = get_ai_response(
        request.message,
        request.session_id
    )

    sentiment = analyze_sentiment(request.message)
    intent = detect_intent(request.message)
    entities = extract_entities(request.message)

    end_time = datetime.now()
    response_time = int((end_time - start_time).total_seconds() * 1000)

    return ChatResponse(
        response=response_text,
        intent=intent,
        sentiment=sentiment,
        entities=entities,
        response_time=response_time
    )


def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of the message"""
    text_lower = text.lower()
    
    positive_words = ["good", "great", "excellent", "happy", "love", "thanks", "thank you", 
                     "awesome", "amazing", "wonderful", "fantastic", "perfect"]
    negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "worst", 
                     "horrible", "poor", "disappointed", "frustrating"]
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

def detect_intent(text: str) -> str:
    """Detect the intent of the message"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["hello", "hi", "hey", "greetings", "good morning", "good evening"]):
        return "greeting"
    elif "?" in text or any(word in text_lower for word in ["what", "how", "why", "when", "where", "who", "which"]):
        return "question"
    elif any(word in text_lower for word in ["thank", "thanks", "appreciate", "grateful"]):
        return "gratitude"
    elif any(word in text_lower for word in ["help", "assist", "support", "need"]):
        return "help_request"
    elif any(word in text_lower for word in ["explain", "tell me", "describe", "define"]):
        return "explanation"
    else:
        return "statement"

def extract_entities(text: str) -> list:
    """Extract entities from text"""
    entities = []
    
    # Email detection
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    for email in emails:
        entities.append({"text": email, "label": "EMAIL"})
    
    # URL detection
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    for url in urls:
        entities.append({"text": url, "label": "URL"})
    
    # Phone number detection
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    phones = re.findall(phone_pattern, text)
    for phone in phones:
        entities.append({"text": phone, "label": "PHONE"})
    
    # Date detection (simple)
    months = ["january", "february", "march", "april", "may", "june", 
              "july", "august", "september", "october", "november", "december"]
    if any(month in text.lower() for month in months):
        entities.append({"text": "date mentioned", "label": "DATE"})
    
    # Number detection
    numbers = re.findall(r'\b\d+\b', text)
    if numbers:
        entities.append({"text": f"{len(numbers)} number(s)", "label": "NUMBER"})
    
    return entities

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 FREE AI Chatbot Backend Starting...")
    print("=" * 60)
    print("✅ No OpenAI API key required!")
    print("✅ CORS enabled")
    print("✅ Running on http://127.0.0.1:8000")
    print("=" * 60)
    print("📝 Endpoints:")
    print("   Health: http://127.0.0.1:8000/health")
    print("   Chat:   http://127.0.0.1:8000/api/chat")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)