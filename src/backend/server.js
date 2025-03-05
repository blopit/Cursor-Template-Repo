/**
 * @fileoverview Backend Server - Simple Express.js server with API endpoint
 * @author Claude
 * @created 2023-11-08
 * 
 * Documentation: .cursor/rules/javascript/server.mdc
 */

const express = require('express');
const cors = require('cors');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// API Routes
app.get('/api/hello', (req, res) => {
  res.json({ 
    message: 'Hello from the backend!',
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`API available at http://localhost:${PORT}/api/hello`);
}); 