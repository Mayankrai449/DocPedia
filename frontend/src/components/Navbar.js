import React, { useState } from 'react';
import './Navbar.css';

const Navbar = ({ handleFileUpload }) => {
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const fileExtension = file.name.split('.').pop().toLowerCase();
      if (fileExtension === 'pdf') {
        setFileName(file.name);
        handleFileUpload(file);
      } else {
        setFileName('');
        setError('Only PDF files are allowed to Upload!');
      }
    } else {
      setFileName('');
      setError('');
    }
  };

  const handleErrorClose = () => {
    setError('');
  };

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-logo">
          <h1>DocPedia</h1>
        </div>
        <span className="file-name">{fileName}</span>
        <div className="upload-btn-wrapper">
          <button className="btn">Choose PDF</button>
          <input type="file" onChange={handleFileChange} />
        </div>
      </nav>
      {error && (
        <div className="flash-error">
          <div>{error}</div>
          <div className="close-btn-wrapper">
            <button className="close-btn" onClick={handleErrorClose}>
              x
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Navbar;