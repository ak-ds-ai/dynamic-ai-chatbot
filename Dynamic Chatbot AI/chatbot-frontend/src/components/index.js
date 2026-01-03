// src/index.js or src/main.jsx
// This is your main React entry point

import React from 'react';
import ReactDOM from 'react-dom/client';

// ⭐ IMPORT TAILWIND CSS - THIS IS IMPORTANT! ⭐
import './index.css';

// Import your chatbot component
import DynamicAIChatbot from './DynamicAIChatbot';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <DynamicAIChatbot />
  </React.StrictMode>
);
