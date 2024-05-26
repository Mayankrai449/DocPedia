import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ChatWindow from './components/ChatWindow';
import axios from 'axios';
import './App.css';

function App() {
  const [pdfs, setPdfs] = useState([]);

  const fetchDocuments = async () => {
    const response = await axios.get('/api/documents');
    setPdfs(response.data);
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('/api/upload', formData);
    setPdfs([...pdfs, response.data]);
  };

  return (
    <div className="app">
      <Navbar handleFileUpload={handleFileUpload} />
      <div className="main-content">
        <ChatWindow pdfs={pdfs} />
      </div>
    </div>
  );
}

export default App;