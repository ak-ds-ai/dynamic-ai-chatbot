import React, { useState, useRef, useEffect } from 'react';
import { Navigate } from "react-router-dom";
import { Send, Bot, User, Trash2, Download, BarChart3, Settings, MessageSquare, TrendingUp, Clock, Smile, Meh, Frown } from 'lucide-react';


const DynamicAIChatbot = () => {
  if (!localStorage.getItem("token")) {
    return <Navigate to="/login" />;
  }
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId] = useState(() => 'session_' + Date.now());
  const [activeTab, setActiveTab] = useState('chat');
  const [analytics, setAnalytics] = useState({
    totalMessages: 0,
    avgResponseTime: 0,
    sentimentStats: { positive: 0, neutral: 0, negative: 0 },
    intentStats: {},
    conversationHistory: []
  });
  const [settings, setSettings] = useState({
    backendUrl: 'http://127.0.0.1:8000',
    enableSentiment: true,
    enableNER: true,
    enableContext: true,
    // Settings to keep:
    theme: 'light',
    autoSave: true,
    chatHistoryLimit: 100,
    showTimestamps: true,
    exportFormat: 'txt',
  });
  const messagesEndRef = useRef(null);
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    checkBackendConnection();
  }, []);

  // Load settings from localStorage on component mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('chatbot-settings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings(parsed);
        console.log('✅ Settings loaded from localStorage');
      } catch (error) {
        console.error('❌ Failed to load settings:', error);
      }
    }
  }, []);

  // Save settings to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chatbot-settings', JSON.stringify(settings));
    console.log('💾 Settings saved to localStorage');
  }, [settings]);

  const checkBackendConnection = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${settings.backendUrl}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });
      if (response.ok) {
        setBackendStatus('connected');
        console.log('✅ Backend connected successfully!');
      } else {
        setBackendStatus('error');
        console.error('Backend returned:', response.status);
      }
    } catch (error) {
      setBackendStatus('error');
      console.error('❌ Backend connection failed:', error);
    }
  };

  useEffect(() => {
    setMessages([{
      id: 1,
      text: "Hello! I'm your Dynamic AI Assistant powered by ChatGPT. I can understand your queries, detect sentiment, extract entities, and provide intelligent responses. How can I help you today?",
      sender: 'bot',
      timestamp: new Date(),
      sentiment: 'neutral'
    }]);
  }, []);

  const callBackendAPI = async (userMessage) => {
    const startTime = Date.now();
    
    try {  const token = localStorage.getItem("token");

      console.log('🚀 Sending request to:', `${settings.backendUrl}/api/chat`);
      console.log('📦 Payload:', { session_id: sessionId, message: userMessage });

      const response = await fetch(`${settings.backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': `Bearer ${localStorage.getItem("token")}`,
},
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage
        })
      });

      console.log('📡 Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Backend error response:', errorText);
        throw new Error(`Backend API error: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Backend response:', data);
      
      const responseTime = Date.now() - startTime;
      
      return { 
        response: data.response,
        intent: data.intent || 'unknown',
        sentiment: data.sentiment || 'neutral',
        entities: data.entities || [],
        responseTime: data.response_time || responseTime
      };
    } catch (error) {
      console.error('💥 Backend API Error:', error);
      const responseTime = Date.now() - startTime;
      
      return {
        response: `⚠️ Error: ${error.message}\n\nPlease check:\n1. Backend is running on ${settings.backendUrl}\n2. CORS is enabled on backend\n3. Check browser console for details`,
        intent: 'error',
        sentiment: 'neutral',
        entities: [],
        responseTime: responseTime,
        isError: true
      };
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: input,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const userInput = input;
    setInput('');
    setIsTyping(true);

    try {
      const result = await callBackendAPI(userInput);
      
      const botMessage = {
        id: messages.length + 2,
        text: result.response,
        sender: 'bot',
        timestamp: new Date(),
        sentiment: result.sentiment,
        intent: result.intent,
        entities: result.entities,
        responseTime: result.responseTime,
        isError: result.isError || false
      };
      
      setMessages(prev => [...prev, botMessage]);
      
      if (!result.isError) {
        updateAnalytics(result.sentiment, result.intent, result.responseTime);
      }
      
    } catch (error) {
      console.error('Error in handleSend:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: "I apologize, but I encountered an error processing your request. Please check the console for details and ensure the backend is running properly.",
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const updateAnalytics = (sentiment, intent, responseTime) => {
    setAnalytics(prev => {
      const newStats = { ...prev };
      newStats.totalMessages += 1;
      newStats.avgResponseTime = Math.round(
        (prev.avgResponseTime * (prev.totalMessages - 1) + responseTime) / prev.totalMessages
      );
      
      newStats.sentimentStats[sentiment] = (newStats.sentimentStats[sentiment] || 0) + 1;
      newStats.intentStats[intent] = (newStats.intentStats[intent] || 0) + 1;
      
      newStats.conversationHistory.push({
        timestamp: new Date(),
        sentiment,
        intent,
        responseTime
      });
      
      return newStats;
    });
  };

  const clearChat = () => {
    setMessages([{
      id: 1,
      text: "Chat cleared. How can I help you?",
      sender: 'bot',
      timestamp: new Date()
    }]);
    setAnalytics({
      totalMessages: 0,
      avgResponseTime: 0,
      sentimentStats: { positive: 0, neutral: 0, negative: 0 },
      intentStats: {},
      conversationHistory: []
    });
  };

  const exportChat = () => {
    const chatLog = messages.map(m => 
      `[${m.timestamp.toLocaleTimeString()}] ${m.sender === 'bot' ? 'Bot' : 'You'}: ${m.text}`
    ).join('\n\n');
    
    const blob = new Blob([chatLog], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-${sessionId}.txt`;
    a.click();
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const resetSettings = () => {
    if (window.confirm('⚠️ Are you sure you want to reset all settings to default? This cannot be undone.')) {
      const defaultSettings = {
        backendUrl: 'http://127.0.0.1:8000',
        enableSentiment: true,
        enableNER: true,
        enableContext: true,
        theme: 'light',
        autoSave: true,
        chatHistoryLimit: 100,
        showTimestamps: true,
        exportFormat: 'txt',
      };
      
      setSettings(defaultSettings);
      localStorage.setItem('chatbot-settings', JSON.stringify(defaultSettings));
      alert('✅ Settings have been reset to default values!');
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch(sentiment) {
      case 'positive': return <Smile className="text-purple-600" size={20} />;
      case 'negative': return <Frown className="text-indigo-600" size={20} />;
      default: return <Meh className="text-indigo-400" size={20} />;
    }
  };

  const getStatusBadge = () => {
    switch(backendStatus) {
      case 'connected':
        return (
          <span className="px-4 py-2 bg-purple-600 text-white rounded-full text-sm font-semibold">
            ✓ Connected
          </span>
        );
      case 'error':
        return (
          <span className="px-4 py-2 bg-indigo-600 text-white rounded-full text-sm font-semibold">
            ✗ Disconnected
          </span>
        );
      default:
        return (
          <span className="px-4 py-2 bg-blue-50 text-indigo-700 rounded-full text-sm font-semibold border-2 border-indigo-200">
            ○ Checking...
          </span>
        );
    }
  };

  const renderChat = () => (
    <div className="flex flex-col h-full bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="flex-1 overflow-y-auto px-8 py-6">
        <div className="max-w-4xl mx-auto space-y-5">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-4 ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
            >
              <div className={`flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center shadow-md ${
                message.sender === 'user'
                  ? 'bg-gradient-to-br from-indigo-600 to-purple-600'
                  : 'bg-white border-2 border-indigo-200'
              }`}>
                {message.sender === 'user' ? (
                  <User className="text-white" size={22} />
                ) : (
                  <Bot className="text-indigo-600" size={22} />
                )}
              </div>
              <div className={`flex-1 ${message.sender === 'user' ? 'flex justify-end' : ''}`}>
                <div
                  className={`max-w-2xl p-5 rounded-2xl shadow-md ${
                    message.sender === 'user'
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                      : message.isError
                      ? 'bg-purple-100 border-2 border-purple-300 text-indigo-900'
                      : 'bg-white border-2 border-indigo-100 text-indigo-900'
                  }`}
                >
                  <p className="text-base leading-relaxed whitespace-pre-wrap">{message.text}</p>
                  {message.sender === 'bot' && !message.isError && (
                    <div className="mt-4 pt-4 border-t border-indigo-100 flex items-center gap-4 text-sm flex-wrap">
                      {message.sentiment && (
                        <div className="flex items-center gap-2">
                          {getSentimentIcon(message.sentiment)}
                          <span className="capitalize font-medium text-indigo-700">
                            {message.sentiment}
                          </span>
                        </div>
                      )}
                      {message.intent && (
                        <span className="px-3 py-1 bg-blue-50 text-indigo-700 rounded-full text-xs font-semibold border border-indigo-200">
                          {message.intent}
                        </span>
                      )}
                      {message.responseTime && (
                        <span className="text-indigo-500 text-xs font-medium">
                          ⚡ {message.responseTime}ms
                        </span>
                      )}
                    </div>
                  )}
                  {message.entities && message.entities.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {message.entities.map((entity, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold border border-purple-300"
                        >
                          {entity.text} ({entity.label})
                        </span>
                      ))}
                    </div>
                  )}
                  <p className={`text-xs mt-3 ${
                    message.sender === 'user' ? 'text-indigo-100' : 'text-indigo-400'
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center bg-white shadow-md border-2 border-indigo-200">
                <Bot className="text-indigo-600" size={22} />
              </div>
              <div className="bg-white border-2 border-indigo-100 rounded-2xl p-5 shadow-md">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                  <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="border-t-2 border-indigo-100 bg-white px-8 py-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              className="flex-1 px-6 py-4 border-2 border-indigo-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-base bg-blue-50 text-indigo-900 placeholder-indigo-400"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim()}
              className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-2xl hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-semibold shadow-md hover:shadow-lg"
            >
              <Send size={22} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAnalytics = () => (
    <div className="h-full overflow-y-auto bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-8 text-indigo-900">Analytics Dashboard</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-2xl p-8 shadow-md border-2 border-indigo-100">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-4 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-xl">
                <MessageSquare className="text-indigo-600" size={28} />
              </div>
              <div>
                <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wider">Total Messages</p>
                <p className="text-4xl font-bold text-indigo-900">{analytics.totalMessages}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-md border-2 border-purple-100">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-4 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-xl">
                <Clock className="text-purple-600" size={28} />
              </div>
              <div>
                <p className="text-sm font-semibold text-purple-600 uppercase tracking-wider">Avg Response</p>
                <p className="text-4xl font-bold text-purple-900">{analytics.avgResponseTime}ms</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-md border-2 border-indigo-100">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-4 bg-gradient-to-br from-indigo-100 to-blue-50 rounded-xl">
                <TrendingUp className="text-indigo-600" size={28} />
              </div>
              <div>
                <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wider">Conversations</p>
                <p className="text-4xl font-bold text-indigo-900">{analytics.conversationHistory.length}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Sentiment Distribution - ONLY purple/indigo colors */}
          <div className="bg-white rounded-2xl p-8 shadow-md border-2 border-indigo-100">
            <h3 className="text-2xl font-bold mb-8 text-indigo-900">Sentiment Distribution</h3>
            <div className="space-y-5">
              {Object.entries(analytics.sentimentStats).map(([sentiment, count]) => (
                <div key={sentiment} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      {getSentimentIcon(sentiment)}
                      <span className="text-lg capitalize font-semibold text-indigo-700">{sentiment}</span>
                    </div>
                    <span className="text-xl font-bold text-indigo-900">{count}</span>
                  </div>
                  <div className="w-full bg-blue-50 rounded-full h-3 border border-indigo-100">
                    <div
                      className="h-3 rounded-full transition-all bg-gradient-to-r from-indigo-500 to-purple-600"
                      style={{ width: `${analytics.totalMessages > 0 ? (count / analytics.totalMessages) * 100 : 0}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Intent Distribution - ONLY purple/indigo colors */}
          <div className="bg-white rounded-2xl p-8 shadow-md border-2 border-purple-100">
            <h3 className="text-2xl font-bold mb-8 text-purple-900">Intent Distribution</h3>
            <div className="space-y-4">
              {Object.entries(analytics.intentStats)
                .sort((a, b) => b[1] - a[1])
                .map(([intent, count]) => (
                  <div key={intent} className="flex justify-between items-center p-5 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl hover:from-indigo-100 hover:to-purple-100 transition-colors border border-indigo-100">
                    <span className="text-lg capitalize font-semibold text-indigo-700">{intent}</span>
                    <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-5 py-2 rounded-full shadow-sm">
                      {count}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div className="h-full overflow-y-auto bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-4xl mx-auto p-8">
        <h2 className="text-3xl font-bold mb-8 text-indigo-900">Settings & Configuration</h2>
        
        {/* Appearance Settings */}
        <div className="bg-white rounded-2xl p-8 shadow-md mb-6 border-2 border-purple-100">
          <h3 className="text-2xl font-bold mb-6 text-purple-900">🎨 Appearance</h3>
          
          <div>
            <label className="block text-base font-semibold text-indigo-700 mb-3">Theme</label>
            <select
              value={settings.theme}
              onChange={(e) => setSettings({...settings, theme: e.target.value})}
              className="w-full px-5 py-4 border-2 border-indigo-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 text-base bg-blue-50 text-indigo-900"
            >
              <option value="light">☀️ Light Mode</option>
              <option value="dark">🌙 Dark Mode (Coming Soon)</option>
              <option value="auto">🔄 Auto (System)</option>
            </select>
            <p className="text-xs text-indigo-500 mt-2">💡 Dark mode will be available in the next update</p>
          </div>
        </div>

        {/* NLP Features */}
        <div className="bg-white rounded-2xl p-8 shadow-md mb-6 border-2 border-indigo-100">
          <h3 className="text-2xl font-bold mb-8 text-indigo-900">🧠 NLP Features</h3>
          <div className="space-y-5">
            <label className="flex items-center justify-between p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl cursor-pointer hover:from-indigo-100 hover:to-purple-100 transition-colors border border-indigo-100">
              <div>
                <p className="font-semibold text-indigo-900 text-lg">Sentiment Analysis</p>
                <p className="text-sm text-indigo-600 mt-2">Detect user emotions and adjust responses</p>
              </div>
              <input
                type="checkbox"
                checked={settings.enableSentiment}
                onChange={(e) => setSettings({...settings, enableSentiment: e.target.checked})}
                className="w-6 h-6 text-purple-600 rounded focus:ring-purple-500"
              />
            </label>

            <label className="flex items-center justify-between p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl cursor-pointer hover:from-indigo-100 hover:to-purple-100 transition-colors border border-indigo-100">
              <div>
                <p className="font-semibold text-indigo-900 text-lg">Named Entity Recognition (NER)</p>
                <p className="text-sm text-indigo-600 mt-2">Extract dates, times, emails, and other entities</p>
              </div>
              <input
                type="checkbox"
                checked={settings.enableNER}
                onChange={(e) => setSettings({...settings, enableNER: e.target.checked})}
                className="w-6 h-6 text-purple-600 rounded focus:ring-purple-500"
              />
            </label>

            <label className="flex items-center justify-between p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl cursor-pointer hover:from-indigo-100 hover:to-purple-100 transition-colors border border-indigo-100">
              <div>
                <p className="font-semibold text-indigo-900 text-lg">Contextual Memory</p>
                <p className="text-sm text-indigo-600 mt-2">Maintain conversation flow and context</p>
              </div>
              <input
                type="checkbox"
                checked={settings.enableContext}
                onChange={(e) => setSettings({...settings, enableContext: e.target.checked})}
                className="w-6 h-6 text-purple-600 rounded focus:ring-purple-500"
              />
            </label>
          </div>
        </div>

        {/* Privacy & Data */}
        <div className="bg-white rounded-2xl p-8 shadow-md mb-6 border-2 border-purple-100">
          <h3 className="text-2xl font-bold mb-8 text-purple-900">🔒 Privacy & Data</h3>
          
          <div className="space-y-5">
            <label className="flex items-center justify-between p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl cursor-pointer hover:from-indigo-100 hover:to-purple-100 transition-colors border border-indigo-100">
              <div>
                <p className="font-semibold text-indigo-900 text-lg">Auto-Save Conversations</p>
                <p className="text-sm text-indigo-600 mt-2">Automatically save chat history to browser</p>
              </div>
              <input
                type="checkbox"
                checked={settings.autoSave}
                onChange={(e) => setSettings({...settings, autoSave: e.target.checked})}
                className="w-6 h-6 text-purple-600 rounded focus:ring-purple-500"
              />
            </label>

            <label className="flex items-center justify-between p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl cursor-pointer hover:from-indigo-100 hover:to-purple-100 transition-colors border border-indigo-100">
              <div>
                <p className="font-semibold text-indigo-900 text-lg">Show Timestamps</p>
                <p className="text-sm text-indigo-600 mt-2">Display message times in chat</p>
              </div>
              <input
                type="checkbox"
                checked={settings.showTimestamps}
                onChange={(e) => setSettings({...settings, showTimestamps: e.target.checked})}
                className="w-6 h-6 text-purple-600 rounded focus:ring-purple-500"
              />
            </label>

            <div>
              <label className="block text-base font-semibold text-indigo-700 mb-3">
                Chat History Limit: <span className="text-purple-600 font-bold">{settings.chatHistoryLimit}</span> messages
              </label>
              <input
                type="range"
                min="10"
                max="500"
                step="10"
                value={settings.chatHistoryLimit}
                onChange={(e) => setSettings({...settings, chatHistoryLimit: parseInt(e.target.value)})}
                className="w-full h-3 bg-indigo-100 rounded-lg appearance-none cursor-pointer accent-purple-600"
              />
              <div className="flex justify-between text-xs text-indigo-600 mt-2">
                <span>10</span>
                <span>250</span>
                <span>500</span>
              </div>
            </div>
          </div>
        </div>

        {/* Export Settings */}
        <div className="bg-white rounded-2xl p-8 shadow-md mb-6 border-2 border-indigo-100">
          <h3 className="text-2xl font-bold mb-6 text-indigo-900">📤 Export Settings</h3>
          
          <div>
            <label className="block text-base font-semibold text-indigo-700 mb-3">Default Export Format</label>
            <select
              value={settings.exportFormat}
              onChange={(e) => setSettings({...settings, exportFormat: e.target.value})}
              className="w-full px-5 py-4 border-2 border-indigo-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 text-base bg-blue-50 text-indigo-900"
            >
              <option value="txt">📝 Plain Text (.txt)</option>
              <option value="json">📊 JSON (.json)</option>
              <option value="csv">📈 CSV (.csv)</option>
              <option value="md">📄 Markdown (.md)</option>
            </select>
          </div>
        </div>

        {/* Settings Info */}
        <div className="bg-blue-50 border-2 border-indigo-200 rounded-xl p-6">
          <p className="text-sm text-indigo-700">
            💡 <strong>Tip:</strong> All settings are automatically saved to your browser and will persist between sessions.
          </p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex flex-col h-screen bg-white">
      <div className="bg-white border-b-2 border-indigo-200">
        <div className="px-8 py-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-4 rounded-2xl shadow-md">
              <Bot className="text-white" size={32} />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Dynamic AI Chatbot
              </h1>
              <p className="text-sm text-indigo-500 font-medium mt-1">NLP • ML • Deep Learning • ChatGPT Integration</p>
            </div>
          </div>
          <div className="flex gap-3">
            <button
              onClick={exportChat}
              className="p-3 text-indigo-600 hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 rounded-xl transition-all"
              title="Export Chat"
            >
              <Download size={22} />
            </button>
            <button
              onClick={clearChat}
              className="p-3 text-purple-600 hover:bg-purple-100 rounded-xl transition-all"
              title="Clear Chat"
            >
              <Trash2 size={22} />
            </button>
          </div>
        </div>

        <div className="flex border-t-2 border-indigo-100">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex-1 px-8 py-5 font-semibold transition-all text-base ${
              activeTab === 'chat'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md'
                : 'text-indigo-600 hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50'
            }`}
          >
            <div className="flex items-center justify-center gap-3">
              <MessageSquare size={22} />
              Chat
            </div>
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex-1 px-8 py-5 font-semibold transition-all text-base ${
              activeTab === 'analytics'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md'
                : 'text-indigo-600 hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50'
            }`}
          >
            <div className="flex items-center justify-center gap-3">
              <BarChart3 size={22} />
              Analytics
            </div>
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`flex-1 px-8 py-5 font-semibold transition-all text-base ${
              activeTab === 'settings'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md'
                : 'text-indigo-600 hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50'
            }`}
          >
            <div className="flex items-center justify-center gap-3">
              <Settings size={22} />
              Settings
            </div>
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        {activeTab === 'chat' && renderChat()}
        {activeTab === 'analytics' && renderAnalytics()}
        {activeTab === 'settings' && renderSettings()}
      </div>
    </div>
  );
};

export default DynamicAIChatbot;