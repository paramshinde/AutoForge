import React from 'react';
import { Folder, FileCode, Database, Terminal, ChevronRight, ChevronDown } from 'lucide-react';

const FileExplorer = ({ activeFile, setActiveFile }) => {
  const files = [
    // NEW STRUCTURE
    { id: 'html', name: 'index.html', type: 'html', path: 'public' },
    { id: 'css', name: 'style.css', type: 'css', path: 'public/css' },
    { id: 'js', name: 'script.js', type: 'js', path: 'public/js' },
    
    { id: 'backend', name: 'main.py', type: 'python', path: 'src/backend' },
    { id: 'database', name: 'schema.sql', type: 'sql', path: 'src/database' },
    { id: 'tests', name: 'test_runner.py', type: 'test', path: 'tests' },
    { id: 'legacy', name: 'legacy_app.py', type: 'python', path: 'legacy' },
  ];
  
  // ... rest of component ...

  return (
    <div className="explorer-pane">
      <div className="border-b" style={{ padding: '12px 16px', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', letterSpacing: '1px' }}>
        EXPLORER
      </div>
      
      <div style={{ padding: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px', color: 'var(--text-primary)', fontSize: '0.9rem' }}>
          <ChevronDown size={14} />
          <span style={{ fontWeight: 600 }}>AUTOFORGE-PROJECT</span>
        </div>

        {/* Tree Items */}
        <div style={{ paddingLeft: '10px', display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {files.map(file => (
            <div 
              key={file.id}
              onClick={() => setActiveFile(file.id)}
              style={{
                display: 'flex', alignItems: 'center', gap: '8px',
                padding: '6px 10px', borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '0.85rem',
                backgroundColor: activeFile === file.id ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                color: activeFile === file.id ? 'var(--accent)' : 'var(--text-secondary)'
              }}
            >
              {file.type === 'react' && <FileCode size={14} color="#61dafb" />}
              {file.type === 'python' && <FileCode size={14} color="#FFD43B" />}
              {file.type === 'sql' && <Database size={14} color="#A0A0A0" />}
              {file.type === 'test' && <Terminal size={14} color="#10b981" />}
              <span>{file.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FileExplorer;