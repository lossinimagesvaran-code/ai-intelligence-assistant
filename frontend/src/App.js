import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';

function App() {
  const [uploadedFiles, setUploadedFiles] = useState({ documents: [], data: [] });
  const [messages, setMessages] = useState([]);

  const handleFileUploaded = (fileInfo) => {
    setUploadedFiles(fileInfo.uploaded_files);
    
    setMessages(prev => [...prev, {
      type: 'system',
      content: fileInfo.message,
      timestamp: new Date().toISOString()
    }]);
  };

  const handleNewMessage = (message) => {
    setMessages(prev => [...prev, message]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Project Intelligence Assistant</h1>
        <p>Upload documents and ask questions using AI-powered analysis</p>
      </header>
      
      <div className="main-container">
        <div className="sidebar">
          <FileUpload onFileUploaded={handleFileUploaded} />
          
          <div className="uploaded-files">
            <h3>Uploaded Files</h3>
            
            {uploadedFiles.documents.length > 0 && (
              <div className="file-section">
                <h4>Documents (PDF)</h4>
                <ul>
                  {uploadedFiles.documents.map((file, idx) => (
                    <li key={idx}> {file}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {uploadedFiles.data.length > 0 && (
              <div className="file-section">
                <h4>Data Files (CSV/Excel)</h4>
                <ul>
                  {uploadedFiles.data.map((file, idx) => (
                    <li key={idx}> {file}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {uploadedFiles.documents.length === 0 && uploadedFiles.data.length === 0 && (
              <p className="no-files">No files uploaded yet</p>
            )}
          </div>
        </div>
        
        <div className="chat-container">
          <ChatInterface 
            messages={messages} 
            onNewMessage={handleNewMessage}
            hasFiles={uploadedFiles.documents.length > 0 || uploadedFiles.data.length > 0}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
