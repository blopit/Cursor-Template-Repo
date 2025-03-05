/**
 * @fileoverview App Component - Main application component
 * @author Claude
 * @created 2023-11-08
 * 
 * Documentation: .cursor/rules/components/app.mdc
 */

import React, { useState } from 'react';

/**
 * App - Main application component with API fetch functionality
 * 
 * @returns {JSX.Element} Rendered component
 */
function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/hello');
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching data');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>Fullstack Example</h1>
      
      <button 
        type="button"
        onClick={fetchData}
        disabled={loading}
        className="fetch-button"
      >
        {loading ? 'Loading...' : 'Fetch Data from API'}
      </button>
      
      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}
      
      {data && (
        <div className="data-display">
          <h2>Response from API:</h2>
          <p><strong>Message:</strong> {data.message}</p>
          <p><strong>Timestamp:</strong> {data.timestamp}</p>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App; 