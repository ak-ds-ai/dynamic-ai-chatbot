import { motion } from "framer-motion";
import { BookOpen, ShieldCheck, Cpu, Layers } from "lucide-react";

const sections = [
  {
    icon: <BookOpen size={28} />,
    title: "What is this Chatbot?",
    text: "An AI-powered chatbot built using FastAPI and a local LLM (Ollama). It supports secure authentication, session memory, and intelligent responses.",
  },
  {
    icon: <ShieldCheck size={28} />,
    title: "Core Features",
    list: [
      "JWT Authentication",
      "Protected Chat & Docs",
      "Local LLM (Ollama)",
      "Session-based Memory",
      "FastAPI Backend",
    ],
  },
  {
    icon: <Cpu size={28} />,
    title: "How It Works",
    list: [
      "User logs in",
      "JWT token is issued",
      "Chat requests are authorized",
      "LLM generates response",
    ],
  },
  {
    icon: <Layers size={28} />,
    title: "Tech Stack",
    list: [
      "Frontend: React + Vite + Tailwind",
      "Backend: FastAPI",
      "Auth: JWT",
      "LLM: Ollama (Local)",
      "DB: SQLAlchemy",
    ],
  },
];

export default function Docs() {
  return (
    <div className="min-h-screen px-8 py-12 bg-gradient-to-br from-indigo-950 via-purple-900 to-slate-900 text-white">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-4xl font-bold mb-12 text-center"
      >
        📘 Documentation
      </motion.h1>

      <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
        {sections.map((sec, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.15 }}
            className="glass rounded-2xl p-6 shadow-xl hover:scale-[1.02] transition-transform"
          >
            <div className="flex items-center gap-4 mb-4 text-primary">
              {sec.icon}
              <h2 className="text-xl font-semibold">{sec.title}</h2>
            </div>

            {sec.text && (
              <p className="text-white/80 leading-relaxed">{sec.text}</p>
            )}

            {sec.list && (
              <ul className="mt-3 space-y-2 text-white/80 list-disc list-inside">
                {sec.list.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
