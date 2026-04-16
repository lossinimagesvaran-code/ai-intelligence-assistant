import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';
import Message from './Message';

function ChatInterface({ messages, onNewMessage, hasFiles }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    if (!hasFiles) {
      onNewMessage({
        type: 'system',
        content: 'Please upload some files before asking questions.',
        timestamp: new Date().toISOString()
      });
      return;
    }

    const userMessage = {
      type: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };
    
    onNewMessage(userMessage);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('/api/query', {
        question: input.trim(),
        session_id: 'default_session'
      });

      const assistantMessage = {
        type: 'assistant',
        content: response.data.answer,
        agent: response.data.agent_used,
        agentType: response.data.agent_type,
        sources: response.data.sources,
        analysis: response.data.analysis,
        timestamp: new Date().toISOString()
      };

      onNewMessage(assistantMessage);
    } catch (err) {
      const errorMessage = {
        type: 'error',
        content: err.response?.data?.detail || 'Error processing query',
        timestamp: new Date().toISOString()
      };
      onNewMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>💬 Chat</h2>
        <p>Ask questions about your uploaded documents and data</p>
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>👋 Welcome!</h3>
            <p>Upload files and start asking questions.</p>
            <div className="example-questions">
              <p><strong>Example questions:</strong></p>
              <ul>
                <li>"What is the main topic of the document?"</li>
                <li>"What is the total budget?"</li>
                <li>"Calculate the average cost"</li>
                <li>"Are there any anomalies in the data?"</li>
              </ul>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}

        {loading && (
          <div className="loading-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>AI is thinking...</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
          className="message-input"
        />
        <button type="submit" disabled={loading || !input.trim()} className="send-button">
          {loading ? '⏳' : '📤'} Send
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;
