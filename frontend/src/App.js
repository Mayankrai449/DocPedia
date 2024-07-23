import React, { useState } from 'react';
import Navbar from './components/Navbar';
import ChatWindow from './components/ChatWindow';
import axiosInstance from './axiosInstance';
import './App.css';

function App() {
  const [pdfs, setPdfs] = useState([]);

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axiosInstance.post('/upload', formData, {  // uploading the file to the backend
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setPdfs([...pdfs, response.data]);
    } catch (error) {
      console.error('Upload error:', error.response ? error.response.data : error.message);
      // Upload Error Handling
    }
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