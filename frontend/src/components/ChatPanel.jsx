import React, { useRef, useEffect } from 'react';
import { Send, Bot, User, Terminal, Cpu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ChatPanel = ({ messages, input, setInput, handleGenerate, loading }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div style={{ width: '400px', background: 'var(--bg-sidebar)', borderRight: '1px solid var(--border)', display: 'flex', flexDirection: 'column' }}>
      
      {/* Header */}
      <div style={{ padding: '20px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Cpu size={20} color="var(--accent)" />
        <span style={{ fontWeight: 600, letterSpacing: '0.5px' }}>AutoForge AI</span>
      </div>

      {/* Messages Area */}
      <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <AnimatePresence>
          {messages.map((msg, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}
            >
              <div style={{ 
                minWidth: '32px', height: '32px', borderRadius: '6px', 
                background: msg.role === 'user' ? '#333' : 'rgba(59, 130, 246, 0.1)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: msg.role === 'user' ? 'white' : 'var(--accent)'
              }}>
                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                  {msg.role === 'user' ? 'You' : 'AutoForge Agent'}
                </div>
                <div style={{ 
                  background: msg.role === 'user' ? 'var(--bg-panel)' : 'transparent',
                  padding: msg.role === 'user' ? '10px' : '0',
                  borderRadius: '8px',
                  fontSize: '0.9rem',
                  lineHeight: '1.5',
                  color: msg.type === 'error' ? 'var(--error)' : msg.type === 'success' ? 'var(--success)' : 'var(--text-primary)'
                }}>
                  {msg.text}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {loading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ display: 'flex', gap: '10px', alignItems: 'center', paddingLeft: '44px', color: 'var(--accent)' }}>
            <Terminal size={14} className="glow-btn" /> Processing...
          </motion.div>
        )}
        <div ref={scrollRef} />
      </div>

      {/* Input Area */}
      <div style={{ padding: '20px', borderTop: '1px solid var(--border)' }}>
        <div style={{ position: 'relative' }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your user story..."
            disabled={loading}
            style={{
              width: '100%', height: '80px', background: '#1a1a1a', border: '1px solid var(--border)',
              borderRadius: '8px', padding: '12px', paddingRight: '40px', color: 'white', resize: 'none', outline: 'none',
              fontFamily: 'inherit'
            }}
            onKeyDown={(e) => { if(e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleGenerate(); }}}
          />
          <button 
            onClick={handleGenerate} 
            disabled={loading || !input.trim()}
            style={{
              position: 'absolute', right: '10px', bottom: '15px', background: 'var(--accent)', 
              border: 'none', borderRadius: '4px', padding: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center',
              opacity: loading ? 0.5 : 1
            }}
          >
            <Send size={16} color="white" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPanel;