import React, { useState, useEffect, useRef } from 'react';
import axiosInstance from '../axiosInstance';
import './ChatWindow.css';

const ChatWindow = ({ pdfs }) => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const [showDefaultText, setShowDefaultText] = useState(true);
  const chatLogRef = useRef(null);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
  
    // Check if the query is empty
    if (!query.trim()) {
      return; // Don't submit if query is empty
    }
    console.log(pdfs);
    if (!pdfs || Object.keys(pdfs).length === 0) {
      setError('No PDF found'); // Show error if no PDF is uploaded
      return;
    }
  
    const newMessage = { sender: 'user', text: query };
    setMessages((prevMessages) => [newMessage, ...prevMessages]);
    setQuery('');
    setIsTyping(true);
    setShowDefaultText(false); // Hide the default text when query is submitted
  
    try {
      const response = await axiosInstance.post('/query', { query });
      const replyMessage = { sender: 'ai', text: response.data.response };
      setMessages((prevMessages) => [replyMessage, ...prevMessages]);
    } catch (error) {
      console.error('Error fetching AI response:', error);
    } finally {
      setIsTyping(false);
    }
  };

  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [messages]);

  const handleErrorClose = () => {
    setError('');
  };

  return (
    <div className="chat-container">
      {error && (
        <div className="flash-error">
          {error}
          <div className='close-btn-wrapper'>
          <button className="close-btn" onClick={handleErrorClose}>
            x
          </button>
          </div>
        </div>
      )}
      <div className="chat-window">
        <div className="chat-log" ref={chatLogRef}>
          {showDefaultText && (
            <div className="default-text">
              <p>Upload your PDF, then explore its depths with our AI-driven Q&A feature! 🤖
              </p>
            </div>
          )}
          {messages.slice().reverse().map((message, index) => (
            <div key={index} className={`chat-message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        <form className="query-box" onSubmit={handleQuerySubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask me..."
          />
          <button type="submit" className="send-btn"></button>
        </form>
        {isTyping && <div className="typing-indicator">. . . .</div>}
      </div>
    </div>
  );
};

export default ChatWindow;