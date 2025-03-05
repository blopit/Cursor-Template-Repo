---
description: JavaScript and Node.js coding style guidelines for Express.js applications
globs: fullstack-example/backend/**/*.js
---
# JavaScript Coding Style Guidelines for Express.js

## Purpose
This document outlines the coding style guidelines for JavaScript and Node.js code in Express.js applications. Following these guidelines ensures consistency, readability, and maintainability across the codebase.

## Code Formatting

### General Rules
- Use 2 spaces for indentation
- Use semicolons at the end of statements
- Use single quotes for strings
- Keep line length under 100 characters
- Use camelCase for variables and functions
- Use PascalCase for classes and constructor functions
- Use UPPER_SNAKE_CASE for constants

### Express.js Specific
- Place route handlers in separate files or modules
- Group related routes together
- Use descriptive names for route handlers
- Chain middleware and route handlers for readability

```javascript
// Good
app.route('/api/users')
  .get(validateToken, getUsers)
  .post(validateToken, validateUser, createUser);

// Avoid
app.get('/api/users', validateToken, getUsers);
app.post('/api/users', validateToken, validateUser, createUser);
```

## Error Handling

- Use async/await with try/catch blocks for asynchronous operations
- Implement a centralized error handling middleware
- Use descriptive error messages
- Include appropriate HTTP status codes

```javascript
// Good
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({
    error: {
      message: err.message || 'Internal Server Error',
      code: err.code || 'INTERNAL_ERROR'
    }
  });
});
```

## API Response Format

- Use consistent JSON response formats
- Include status indicators in the response
- Provide meaningful error messages
- Include timestamps for time-sensitive operations

```javascript
// Success response format
{
  "success": true,
  "data": { ... },
  "timestamp": "2023-11-08T12:34:56.789Z"
}

// Error response format
{
  "success": false,
  "error": {
    "message": "Resource not found",
    "code": "NOT_FOUND"
  },
  "timestamp": "2023-11-08T12:34:56.789Z"
}
```

## Comments and Documentation

- Use JSDoc for documenting functions and modules
- Include purpose, parameters, and return values
- Document API endpoints with examples
- Keep comments up-to-date with code changes

## Performance Considerations

- Use asynchronous operations where appropriate
- Implement proper caching strategies
- Optimize database queries
- Use compression middleware for responses
- Implement rate limiting for public APIs 
