import React, { useState } from 'react';
import './Message.css';

function Message({ message }) {
  const [showSources, setShowSources] = useState(false);

  const renderContent = () => {
    if (message.type === 'system') {
      return (
        <div className="message system-message">
          <div className="message-icon">ℹ️</div>
          <div className="message-content">
            <p>{message.content}</p>
          </div>
        </div>
      );
    }

    if (message.type === 'error') {
      return (
        <div className="message error-message">
          <div className="message-icon">⚠️</div>
          <div className="message-content">
            <p>{message.content}</p>
          </div>
        </div>
      );
    }

    if (message.type === 'user') {
      return (
        <div className="message user-message">
          <div className="message-content">
            <p>{message.content}</p>
          </div>
          <div className="message-icon">👤</div>
        </div>
      );
    }

    if (message.type === 'assistant') {
      return (
        <div className="message assistant-message">
          <div className="message-icon">🤖</div>
          <div className="message-content">
            <div className="agent-badge">
              {message.agentType === 'document_qa' ? '📄' : '📊'} {message.agent}
            </div>
            
            <p className="answer-text">{message.content}</p>

            {message.sources && message.sources.length > 0 && (
              <div className="sources-section">
                <button 
                  className="sources-toggle"
                  onClick={() => setShowSources(!showSources)}
                >
                  {showSources ? '▼' : '▶'} Sources ({message.sources.length})
                </button>
                
                {showSources && (
                  <div className="sources-list">
                    {message.sources.map((source, idx) => (
                      <div key={idx} className="source-item">
                        <div className="source-header">
                          <strong>📄 {source.source}</strong>
                          <span className="chunk-id">Chunk {source.chunk_id}</span>
                        </div>
                        <p className="source-preview">{source.content}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {message.analysis && (
              <div className="analysis-section">
                <h4>📊 Analysis Details</h4>
                <pre>{JSON.stringify(message.analysis, null, 2)}</pre>
              </div>
            )}
          </div>
        </div>
      );
    }

    return null;
  };

  return renderContent();
}

export default Message;
