import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Send, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../logo.png';

const Chatbot = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const selectedCourse = location.state?.selectedCourse;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMessage = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    setMessages(prev => [...prev, { role: 'user', content: newMessage }]);

    try {
      const response = await axios.post('http://127.0.0.1:5000/ai/chatbot', {
        message: newMessage,
        storage_path: `${selectedCourse.name.toLowerCase().replace(/\s/g, '_')}_db`
      });

      setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const MessageBubble = ({ message }) => {
    if (message.role === 'user') {
      return (
        <div className="flex justify-end mb-4">
          <div className="bg-[#9E72C3] text-white rounded-2xl py-3 px-4 max-w-[70%]">
            {message.content}
          </div>
        </div>
      );
    }

    return (
      <div className="flex items-start mb-4">
        <div className="w-10 h-10 rounded-full border-4 border-purple-200 bg-white overflow-hidden flex-shrink-0 mr-3">
          <img src={logo} alt="AI Assistant" className="w-full h-full" />
        </div>
        <div className="bg-gray-200 rounded-2xl py-3 px-4 max-w-[70%]">
          {message.content}
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="bg-white shadow-sm px-6 py-4 flex items-center">
        <button 
          onClick={() => navigate('/')}
          className="p-2 hover:bg-gray-100 rounded-full"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-xl font-semibold ml-4">{selectedCourse?.name} Assistant</h1>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6">
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
        {isLoading && (
          <div className="flex items-start">
            <div className="w-8 h-8 rounded-full overflow-hidden flex-shrink-0 bg-gray-200 mr-2">
              <img src={logo} alt="AI Assistant" className="w-full h-full object-cover" />
            </div>
            <div className="bg-gray-200 rounded-2xl py-3 px-4">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-3 border border-gray-300 rounded-full focus:outline-none focus:border-[#9E72C3]"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className={`p-3 rounded-full ${
              isLoading || !inputMessage.trim()
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-[#9E72C3] hover:bg-[#9E72C3]'
            } text-white`}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;