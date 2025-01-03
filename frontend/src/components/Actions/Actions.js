import React, { useState } from "react";
import axios from "axios";
import "./Actions.css";
import httpClient from "../../httpClient";

const Actions = () => {
  const [files, setFiles] = useState([]);
  const [textInput, setTextInput] = useState("");
  const [textInputName, setTextInputName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);  // New loading state
  const [responseText, setResponseText] = useState("");  // State to store the API response

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const validFiles = selectedFiles.filter((file) =>
      [".xlsx", ".xls"].includes(file.name.slice(-5).toLowerCase())
    );

    if (validFiles.length < selectedFiles.length) {
      setError("Only .xlsx and .xls files are allowed.");
      setTimeout(() => setError(""), 3000); // Clear error after 3 seconds
    }

    setFiles(validFiles);
  };

  

  const handleGenerateQuery = async () => {
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('user_id');

    if (!files.length) {
      setError("Please upload at least one file.");
      return;
    }

    if (!textInput.trim()) {
      setError("Please enter some text.");
      return;
    }

    if (!textInputName.trim()) {
      setError("Please enter some text.");
      return;
    }

    const formData = new FormData();
    files.forEach((file) => formData.append("attachments", file));
    formData.append("user_query", textInput);
    formData.append("usecase", textInputName);
    formData.append("user_id", user_id);

    // Set loading state to true when starting the API request
    setLoading(true);
    setResponseText("");  // Clear previous response

    try {
        const response = await httpClient.post('/upload_files', formData); // Sending only email and password
        const res = response.data;
          
      } catch (error) {
        setError('Failed.');
        console.error('Error:', error);
        // Handle network or other errors
      }
    };

  // Function to handle copying text to clipboard
  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(responseText).then(() => {
      alert("Text copied to clipboard!");
    }).catch(err => {
      console.error("Error copying text: ", err);
    });
  };

  return (
    <div className="about-section">
      {/* File Upload Section */}
      <div className="upload-and-input-section">
        <div className="file-upload-section">
          <h4>Upload Files</h4>
          <input
            type="file"
            accept=".xlsx,.xls"
            multiple
            onChange={handleFileChange}
            disabled={loading} // Disable input when loading
          />
          {error && <div className="error-popup">{error}</div>}

          {files.length > 0 && (
            <div className="file-names-container">
              <ul>
                {files.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>


        <div className="text-input-section">
          <h4>Enter Usecase</h4>
          <textarea
            placeholder="Type something here..."
            className="stylish-text-input"
            rows="1"
            onInput={(e) => {
              e.target.style.height = "auto"; // Reset height
              e.target.style.height = `${e.target.scrollHeight}px`; // Adjust height
            }}
            value={textInputName}
            onChange={(e) => setTextInputName(e.target.value)}
            disabled={loading} // Disable input when loading
          />
        </div>

        <div className="text-input-section">
          <h4>Your Needs Here...</h4>
          <textarea
            placeholder="Type something here..."
            className="stylish-text-input"
            rows="1"
            onInput={(e) => {
              e.target.style.height = "auto"; // Reset height
              e.target.style.height = `${e.target.scrollHeight}px`; // Adjust height
            }}
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            disabled={loading} // Disable input when loading
          />
        </div>

        <button
          className="generate-query-button"
          onClick={handleGenerateQuery}
          disabled={loading} // Disable button when loading
        >
          {loading ? "Generating..." : "Generate Query"}
        </button>

        {/* Loading Overlay */}
        {loading && (
          <div className="loading-overlay">
            <div className="loading-spinner"></div>
            <p>Loading...</p>
          </div>
        )}
      </div>

      {/* Response Section */}
      {responseText && (
        <div className="response-section">
          <h4>API Response</h4>
          <div className="response-text-container">
            <p>{responseText}</p>
          </div>
          <button className="copy-button" onClick={handleCopyToClipboard}>
            Copy
          </button>
        </div>
      )}
    </div>
  );
};

export default Actions;
