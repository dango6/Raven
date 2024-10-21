import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file for styling

function App() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const chatBoxRef = useRef(null);

  // Simulating receiving a message
  const receiveMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, { content: message, sender: 'received' }]);
  };

  const handleSendMessage = async () => {
    if (message.trim()) {
      // Add the sent message to the chat
      setMessages([...messages, { content: message, sender: 'sent' }]);
      setMessage('');
  
      // Send the message to the backend
      try {
        const response = await axios.post('/api/messages', { content: message });
        
        // Display the response message as "received"
        if (response.data && response.data.reply) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { content: response.data.reply, sender: 'received' },
          ]);
        }
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chat-container">
      <h1>Raven Messaging</h1>
      <div className="chat-box" ref={chatBoxRef}> {/* Attach the ref to the chat box */}
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === 'sent' ? 'sent' : 'received'}`}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress} // Listen for the 'Enter' key
          placeholder="Type a message"
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;