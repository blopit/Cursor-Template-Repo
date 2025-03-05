/**
 * @fileoverview Main Entry Point - React application entry point
 * @author Claude
 * @created 2023-11-08
 * 
 * Documentation: .cursor/rules/javascript/main.mdc
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); 