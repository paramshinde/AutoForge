import React, { useState } from 'react';
import axios from 'axios';
import ChatPanel from './components/ChatPanel';
import Workbench from './components/Workbench';
import './App.css';

function App() {
  const [activeFile, setActiveFile] = useState('html');
  const [input, setInput] = useState("As a user, I want a login page so I can access the system.");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'agent', text: 'AutoForge initialized. Describe your full-stack app.' }
  ]);
  const [artifacts, setArtifacts] = useState(null);

  const handleGenerate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: 'user', text: input }]);
    setArtifacts(null);

    const steps = [
      { t: 800, msg: "Parsing User Story..." },
      { t: 1800, msg: " Architect Agent: Refining requirements..." },
      { t: 3000, msg: "Orchestrating Agents..." },
      

      { t: 4500, msg: " Frontend Agent: Generating React/HTML UI..." },
      { t: 4500, msg: " Backend Agent: Building FastAPI Routes..." }, 
      
      { t: 6000, msg: "Running Unit Tests in Sandbox..." },
      { t: 7000, msg: " Build Successful.", type: 'success' }
    ];

    steps.forEach(({ t, msg, type }) => {
      setTimeout(() => setMessages(prev => [...prev, { role: 'agent', text: msg, type }]), t);
    });

    try {
      const response = await axios.post('http://localhost:8000/generate', { user_story: input });
      
      // Wait for animation to finish before showing code
      setTimeout(() => {
        setArtifacts(response.data);
        setLoading(false);
        setActiveFile('html'); // Auto-open the main file
      }, 7000); 
    } catch (error) {
      setTimeout(() => {
        setLoading(false);
        setMessages(prev => [...prev, { role: 'agent', text: 'Error connecting to backend.', type: 'error' }]);
      }, 2000);
    }
  };

  return (
    <div className="app-layout">
      {/* 1. Chat Panel (Left) */}
      <ChatPanel 
        messages={messages} 
        input={input} 
        setInput={setInput} 
        handleGenerate={handleGenerate} 
        loading={loading} 
      />
      
      {/* 2. Workbench (Right) - Contains Explorer, Editor, Preview, Download */}
      <Workbench 
        activeFile={activeFile} 
        setActiveFile={setActiveFile}
        artifacts={artifacts} 
        userStory={input} // 👈 Critical for Smart Preview logic
      />
    </div>
  );
}

export default App;