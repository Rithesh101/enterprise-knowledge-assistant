import React from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import ChatWindow from '../components/ChatWindow';

const ChatPage = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  let user = { email: '', department: '' };

if (token) {
  const decodedToken = jwtDecode(token);
  user.email = decodedToken.sub;
  user.department = decodedToken.department;
}

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="chat-page">
      <header className="chat-header">
        <h1>Enterprise Knowledge Assistant</h1>
        <div className="user-info">
          <span>Welcome, {user.email} ({user.department})</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>
      <ChatWindow />
    </div>
  );
};

export default ChatPage;