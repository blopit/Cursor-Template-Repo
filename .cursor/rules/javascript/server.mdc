---
description: Documentation for the Express.js backend server
globs: fullstack-example/backend/server.js
alwaysApply: true
---
# Backend Server Documentation

## Purpose
This file implements a simple Express.js server that provides an API endpoint for the frontend to interact with. It demonstrates basic backend functionality including middleware setup, route handling, and response formatting.

## Usage
The server can be started using the following commands:

```bash
# Start the server in development mode
npm run dev

# Start the server in production mode
npm start
```

The server exposes the following API endpoints:

- `GET /api/hello`: Returns a JSON response with a greeting message and timestamp

Example API response:
```json
{
  "message": "Hello from the backend!",
  "timestamp": "2023-11-08T12:34:56.789Z"
}
```

## Dependencies
List of dependencies and relationships with other files/components:

- `express`: Web framework for Node.js
- `cors`: Middleware to enable Cross-Origin Resource Sharing
- Frontend application: Consumes the API endpoints provided by this server

## Maintenance
Guidelines for maintaining and updating this file:

- Add new API endpoints as needed following the established pattern
- Update CORS settings if additional origins need to be allowed
- Consider adding error handling middleware for production use
- Implement request validation for more complex endpoints

## Additional Notes

### Port Configuration
The server runs on port 8000 by default, following the port standardization guidelines. This can be overridden by setting the `PORT` environment variable.

### Security Considerations
For a production environment, consider:
- Adding rate limiting
- Implementing proper authentication
- Using HTTPS
- Adding input validation

