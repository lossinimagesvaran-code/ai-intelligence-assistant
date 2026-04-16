import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function FileUpload({ onFileUploaded }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onFileUploaded(response.data);
      setSelectedFile(null);
      
      document.getElementById('file-input').value = '';
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading file');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <h3>📤 Upload Files</h3>
      
      <div className="upload-area">
        <input
          id="file-input"
          type="file"
          accept=".pdf,.csv,.xlsx,.xls"
          onChange={handleFileSelect}
          disabled={uploading}
        />
        
        {selectedFile && (
          <div className="selected-file">
            <span>✓ {selectedFile.name}</span>
          </div>
        )}
        
        <button
          onClick={handleUpload}
          disabled={!selectedFile || uploading}
          className="upload-button"
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="file-info">
        <p>Supported formats:</p>
        <ul>
          <li>PDF documents</li>
          <li>CSV files</li>
          <li>Excel files (.xlsx, .xls)</li>
        </ul>
      </div>
    </div>
  );
}

export default FileUpload;
