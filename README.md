# 🤖 Dynamic AI Chatbot

A **full-stack AI chatbot application** built with **FastAPI** and **React**, featuring **JWT authentication**, **protected routes**, **session-based chat**, and **local LLM support (Ollama)**.  
Designed with a **modern UI**, **dark/light theme**, and a **scalable backend architecture**.

---

## 🚀 Features

### 🔐 Authentication & Security
- JWT-based authentication
- Secure login & registration
- Protected Chat & Documentation routes
- Token-based session handling

### 🧠 AI Capabilities
- Local LLM integration using **Ollama**
- Intelligent response generation
- Session-based conversation memory
- Extensible NLP services

### 🎨 Frontend (React)
- Modern landing page
- Animated login & register UI
- Dark / Light theme toggle
- Protected routing with React Router
- Clean navigation (Chat, Docs, Logout)

### ⚙️ Backend (FastAPI)
- RESTful API architecture
- SQLAlchemy ORM
- MySQL database
- JWT utilities & dependency injection
- Modular service design

---

## 🧱 Tech Stack

### Backend
- **FastAPI**
- **Python 3.11+**
- **SQLAlchemy**
- **MySQL**
- **JWT (JSON Web Tokens)**
- **Ollama (Local LLM)**

### Frontend
- **React (Vite)**
- **React Router**
- **Framer Motion**
- **Tailwind / CSS Variables**
- **Modern Glassmorphism UI**

---

## 📂 Project Structure

```text
Dynamic Chatbot AI updated/
│
├── Backend/
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── jwt_utils.py
│   ├── models.py
│   ├── main.py
│   └── ...
│
├── chatbot-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── .gitignore
└── README.md


⚡ Getting Started
1️⃣ Clone Repository
git clone https://github.com/your-username/dynamic-ai-chatbot.git
cd dynamic-ai-chatbot

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Variables (Backend/.env)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai_chatbot
SECRET_KEY=your_secret_key
ALGORITHM=HS256

5️⃣ Run Backend
uvicorn main:app --reload


API runs at:

http://127.0.0.1:8000


Swagger Docs:

http://127.0.0.1:8000/docs

🌐 Frontend Setup
6️⃣ Install Dependencies
cd chatbot-frontend
npm install

7️⃣ Run Frontend
npm run dev


Frontend runs at:

http://localhost:5173

🔐 Authentication Flow

User registers

User logs in

JWT token stored in localStorage

Protected routes validate token

Chat & Docs unlocked

📖 Documentation Page

Explains system architecture

Authentication flow

AI workflow

Backend & frontend interaction

Designed as a developer-friendly reference

🧪 Testing

API tests

Database connection tests

NLP service tests

🛡 Security Notes

.env excluded via .gitignore

Passwords hashed securely

JWT-based stateless authentication

Backend routes protected via dependencies


---


