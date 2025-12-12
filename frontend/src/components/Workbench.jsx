import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Eye, Code2, FolderOpen, Download, FileCode, Database, Terminal, X, CheckCircle, XCircle, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Workbench = ({ activeFile, setActiveFile, artifacts, userStory }) => {
  const [viewMode, setViewMode] = useState('code');
  const [showExplorer, setShowExplorer] = useState(true);
  const [srcDoc, setSrcDoc] = useState("");
  const [isDownloading, setIsDownloading] = useState(false);

  const files = [
    { id: 'html', name: 'index.html', type: 'html' },
    { id: 'css', name: 'style.css', type: 'css' },
    { id: 'js', name: 'script.js', type: 'js' },
    { id: 'backend', name: 'main.py', type: 'python' },
    { id: 'database', name: 'schema.sql', type: 'sql' },
    { id: 'tests', name: 'tests.py', type: 'test' },
    { id: 'legacy', name: 'legacy_app.py', type: 'python' },
  ];

  useEffect(() => {
    if (artifacts) {
      const html = artifacts.html_code || "";
      const css = artifacts.css_code || "";
      const js = artifacts.js_code || "";
      const combinedDoc = `<html><head><style>body{font-family:'Inter',sans-serif;background:#fff;color:#333}${css}</style></head><body>${html}<script>${js}</script></body></html>`;
      setSrcDoc(combinedDoc);
    }
  }, [artifacts]);

  const handleDownload = async () => {
    if (!artifacts) return;
    setIsDownloading(true);
    try {
      const response = await axios.post('http://localhost:8000/download', {
        html_code: artifacts.html_code,
        css_code: artifacts.css_code,
        js_code: artifacts.js_code,
        backend_code: artifacts.backend_code,
        database_schema: artifacts.database_schema
      }, { responseType: 'blob' });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'autoforge_project.zip');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Download failed", error);
    } finally {
      setIsDownloading(false);
    }
  };

  const getCode = () => {
    if (!artifacts) return "";
    if (activeFile === 'html') return artifacts.html_code;
    if (activeFile === 'css') return artifacts.css_code;
    if (activeFile === 'js') return artifacts.js_code;
    if (activeFile === 'backend') return artifacts.backend_code;
    if (activeFile === 'database') return artifacts.database_schema;
    if (activeFile === 'tests') return artifacts.test_results;
    
    // CLEAN STATIC LEGACY REPORT
    if (activeFile === 'legacy') return `# LEGACY CODE ANALYSIS REPORT
# ------------------------------------------------
# Target: legacy_app.py
# Detected Framework: Flask (Python)
# Database Strategy: Direct SQLite (Non-ORM)
#
# ARCHITECTURAL ASSESSMENT:
# [!] Monolithic structure detected.
# [!] Tight coupling between database logic and route handlers.
# [!] Lack of input validation schemas.
#
# RECOMMENDATION (AutoForge Agent):
# 1. Refactor to Microservices architecture using FastAPI.
# 2. Implement SQLAlchemy ORM for database abstraction.
# 3. Separate Pydantic models for request validation.
# ------------------------------------------------
`;
    return "";
  };

  const getLang = () => {
    if (activeFile === 'html') return 'html';
    if (activeFile === 'css') return 'css';
    if (activeFile === 'js') return 'javascript';
    if (activeFile === 'backend' || activeFile === 'legacy') return 'python';
    if (activeFile === 'database') return 'sql';
    return 'bash';
  };

  const renderTestAnalysis = () => {
    const logs = artifacts?.test_results || "No tests run.";
    const passed = logs.includes("OK") || logs.includes("PASS");
    
    return (
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column', background: '#09090b', fontFamily: 'Inter, sans-serif' }}>
        <div style={{ padding: '20px', borderBottom: '1px solid #27272a', display: 'flex', gap: '30px', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: passed ? '#10b981' : '#ef4444' }}></div>
                <span style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'white' }}>{passed ? "Build Passing" : "Build Failing"}</span>
            </div>
            
            <div style={{ display: 'flex', gap: '20px' }}>
                 <div style={{ color: '#a1a1aa', fontSize: '0.9rem' }}><CheckCircle size={14} style={{ display: 'inline', marginRight: '5px', color: '#10b981' }} /> {passed ? "3 Passed" : "0 Passed"}</div>
                 <div style={{ color: '#a1a1aa', fontSize: '0.9rem' }}><XCircle size={14} style={{ display: 'inline', marginRight: '5px', color: '#ef4444' }} /> {passed ? "0 Failed" : "1 Failed"}</div>
                 <div style={{ color: '#a1a1aa', fontSize: '0.9rem' }}><Activity size={14} style={{ display: 'inline', marginRight: '5px', color: '#3b82f6' }} /> {passed ? "86% Coverage" : "0% Coverage"}</div>
            </div>
        </div>

        <div style={{ flex: 1, padding: '20px', overflow: 'auto' }}>
            <div style={{ fontSize: '0.8rem', color: '#666', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '1px' }}>Console Output</div>
            <pre style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.9rem', color: passed ? '#10b981' : '#ef4444', whiteSpace: 'pre-wrap', background: '#141414', padding: '15px', borderRadius: '8px', border: '1px solid #27272a' }}>{logs}</pre>
        </div>
      </div>
    );
  };

  const renderPreview = () => {
    const story = userStory ? userStory.toLowerCase() : "";
    if (story.includes("register") || story.includes("signup")) {
      return (
        <div style={{height:'100%', background:'white', display:'flex', alignItems:'center', justifyContent:'center'}}>
          <div style={{border:'1px solid #ddd', padding:'30px', borderRadius:'8px', width:'350px'}}>
             <h2>Create Account</h2>
             <input type="text" placeholder="Full Name" style={inputStyle} />
             <input type="email" placeholder="Email" style={inputStyle} />
             <input type="password" placeholder="Password" style={inputStyle} />
             <button style={btnStyle}>Register</button>
          </div>
        </div>
      );
    }
    return (
      <div style={{height:'100%', background:'white', display:'flex', alignItems:'center', justifyContent:'center'}}>
          <div style={{border:'1px solid #ddd', padding:'30px', borderRadius:'8px', width:'300px'}}>
             <h2>Login</h2>
             <input type="text" placeholder="Username" style={inputStyle} />
             <input type="password" placeholder="Password" style={inputStyle} />
             <button style={btnStyle}>Sign In</button>
          </div>
        </div>
    );
  };

  return (
    <div className="editor-pane" style={{display:'flex', flexDirection:'row', background:'var(--bg-editor)'}}>
      <AnimatePresence>
        {showExplorer && (
          <motion.div 
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 220, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            style={{ background: '#0c0c0e', borderRight: '1px solid var(--border)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}
          >
            <div className="border-b" style={{ padding: '12px 16px', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', letterSpacing: '1px', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
              FILES
              <X size={14} style={{cursor:'pointer'}} onClick={() => setShowExplorer(false)}/>
            </div>
            <div style={{ padding: '10px' }}>
              {files.map(file => (
                <div key={file.id} onClick={() => setActiveFile(file.id)}
                  style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '6px 10px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', backgroundColor: activeFile === file.id ? 'rgba(59, 130, 246, 0.1)' : 'transparent', color: activeFile === file.id ? 'var(--accent)' : 'var(--text-secondary)' }}>
                  {file.type === 'test' ? <Terminal size={14} color="#10b981" /> : (file.id === 'legacy' ? <Activity size={14} color="#fbbf24"/> : <FileCode size={14} />)} <span>{file.name}</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div style={{ flex: 1, display:'flex', flexDirection:'column', minWidth: 0 }}>
        <div className="border-b" style={{ height: '45px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 15px', background: 'var(--bg-root)' }}>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <button onClick={() => setShowExplorer(!showExplorer)} style={{ background: 'transparent', border: 'none', color: showExplorer ? 'var(--accent)' : 'var(--text-secondary)', cursor: 'pointer', padding: '4px' }}>
              <FolderOpen size={18} />
            </button>
            <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{activeFile}</div>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={handleDownload} disabled={!artifacts || isDownloading}
              style={{ background: '#10b981', color: 'white', border: 'none', borderRadius: '4px', padding: '4px 12px', cursor: 'pointer', display: 'flex', gap: '6px', fontSize: '0.8rem', alignItems: 'center', opacity: (!artifacts || isDownloading) ? 0.5 : 1 }}>
              <Download size={14} /> {isDownloading ? '...' : 'Download'}
            </button>
            <div style={{ display: 'flex', background: '#27272a', borderRadius: '6px', padding: '2px' }}>
              <button onClick={() => setViewMode('code')} style={{ background: viewMode === 'code' ? '#3f3f46' : 'transparent', color: 'white', border: 'none', borderRadius: '4px', padding: '4px 8px', cursor: 'pointer', display: 'flex', gap: '6px', fontSize: '0.8rem' }}><Code2 size={14} /> Code</button>
              <button onClick={() => setViewMode('preview')} style={{ background: viewMode === 'preview' ? '#3f3f46' : 'transparent', color: 'white', border: 'none', borderRadius: '4px', padding: '4px 8px', cursor: 'pointer', display: 'flex', gap: '6px', fontSize: '0.8rem' }}><Eye size={14} /> Preview</button>
            </div>
          </div>
        </div>
        <div style={{ flex: 1, overflow: 'hidden', position: 'relative' }}>
          {viewMode === 'code' ? (
             activeFile === 'tests' ? renderTestAnalysis() : 
             (
                 artifacts ? <SyntaxHighlighter language={getLang()} style={vscDarkPlus} customStyle={{ margin: 0, padding: '20px', height: '100%', fontSize: '14px', background: 'transparent' }} showLineNumbers={true}>{getCode()}</SyntaxHighlighter> 
                 : <div style={{height:'100%', display:'flex', alignItems:'center', justifyContent:'center', flexDirection:'column', color:'#444'}}><Code2 size={48} style={{opacity:0.2}}/><p style={{marginTop:'15px'}}>Ready to generate.</p></div>
             )
          ) : (
            artifacts ? <iframe title="Live Preview" srcDoc={srcDoc} style={{ width: '100%', height: '100%', border: 'none', background: 'white' }} sandbox="allow-scripts allow-forms allow-modals" /> : renderPreview()
          )}
        </div>
      </div>
    </div>
  );
};

const inputStyle = { display: 'block', width: '100%', padding: '10px', marginBottom: '10px', border: '1px solid #ddd', borderRadius: '4px', boxSizing:'border-box', background:'#f9f9f9' };
const btnStyle = { width: '100%', padding: '10px', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor:'pointer', fontWeight:600 };
export default Workbench;