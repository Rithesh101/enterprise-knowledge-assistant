import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ChatPage from './pages/ChatPage';

const App = () => {
  const token = localStorage.getItem('token');

  return (
    <div className="container">
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route 
          path="/chat" 
          element={token ? <ChatPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="*" 
          element={<Navigate to={token ? "/chat" : "/login"} />} 
        />
      </Routes>
    </div>
  );
};

export default App;