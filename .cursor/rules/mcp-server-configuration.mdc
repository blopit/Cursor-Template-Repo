---
description: Configuration guidelines for MCP Server based on Express.js
globs: mcp-server/**/*.js, mcp-server/**/*.json
---
# MCP Server Configuration Guidelines

## Purpose
This document outlines the configuration standards and best practices for the MCP Server, which is built on Express.js. It provides guidance on environment setup, security configurations, and deployment considerations.

## Environment Configuration

### Environment Variables
The MCP Server uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

```
# Server Configuration
PORT=8000
NODE_ENV=development

# Security
JWT_SECRET=your_jwt_secret_key
CORS_ORIGIN=http://localhost:3000

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mcp_dev
DB_USER=postgres
DB_PASSWORD=postgres
```

For production environments, ensure these variables are set securely in your deployment platform.

## Server Configuration

### Port Settings
- Default port: 8000
- Override with PORT environment variable
- Follow port standardization guidelines for different environments:
  - Development: 8000
  - Testing: 8001
  - Production: Configurable based on deployment

### CORS Configuration
Configure CORS to allow requests only from trusted origins:

```javascript
const corsOptions = {
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
};

app.use(cors(corsOptions));
```

## Security Considerations

### Authentication
- Use JWT (JSON Web Tokens) for authentication
- Implement token refresh mechanism
- Store tokens securely (HTTP-only cookies)
- Set appropriate token expiration times

### Data Validation
- Validate all input data using a library like Joi or express-validator
- Sanitize inputs to prevent injection attacks
- Implement request rate limiting

### Error Handling
- Use a centralized error handling middleware
- Log errors securely (avoid exposing sensitive information)
- Return appropriate HTTP status codes
- Provide meaningful error messages to clients

## Performance Optimization

### Caching
- Implement response caching for frequently accessed data
- Use memory caching for session data
- Consider Redis for distributed caching in production

### Compression
- Enable compression middleware for all responses
- Configure appropriate compression levels

```javascript
app.use(compression({
  level: 6, // Balanced between speed and compression ratio
  threshold: 0 // Compress all responses
}));
```

## Deployment Guidelines

### Production Checklist
- Set NODE_ENV to 'production'
- Enable HTTPS
- Configure proper logging
- Set up monitoring and alerting
- Implement horizontal scaling if needed

### Container Deployment
- Use Docker for containerization
- Follow the principle of immutable infrastructure
- Implement health checks
- Configure appropriate resource limits

## Maintenance

- Regularly update dependencies
- Monitor for security vulnerabilities
- Implement automated testing
- Document API changes
- Maintain backward compatibility when possible 
