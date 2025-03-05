---
description: Environment configuration guidelines for Express.js applications
globs: fullstack-example/**/.env*, fullstack-example/**/*.config.js
---
# Environment Configuration Guidelines

## Purpose
This document outlines best practices for environment configuration in Express.js applications. It provides guidance on managing environment variables, configuration files, and environment-specific settings.

## Environment Types

### Development Environment
- Used for local development
- Debug logging enabled
- Detailed error messages
- No rate limiting
- Local database connections
- CORS configured for local frontend

### Testing Environment
- Used for automated tests
- Minimal logging
- In-memory or test-specific databases
- Mocked external services
- Isolated from development and production

### Staging Environment
- Mirror of production
- Used for final testing before deployment
- Production-like data (anonymized)
- Same infrastructure as production
- Restricted access

### Production Environment
- Live application environment
- Error-only logging (with monitoring)
- Performance optimized
- Security hardened
- Rate limiting enabled
- Restricted CORS settings

## Environment Variables

### Variable Naming
- Use uppercase with underscores
- Use prefixes for grouping related variables
- Be descriptive but concise

```
# Good
DATABASE_HOST=localhost
DATABASE_PORT=5432
JWT_SECRET=your_secret_key

# Avoid
DBHOST=localhost
DB_P=5432
SECRET=your_secret_key
```

### Environment Files
Use different `.env` files for different environments:

- `.env`: Default environment variables (committed with defaults)
- `.env.development`: Development-specific overrides (not committed)
- `.env.test`: Test-specific overrides (committed)
- `.env.production`: Production-specific overrides (not committed)

Example `.env` file:
```
# Server Configuration
PORT=8000
NODE_ENV=development
LOG_LEVEL=debug

# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=app_dev
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Security
JWT_SECRET=development_secret
JWT_EXPIRATION=1d
CORS_ORIGIN=http://localhost:3000
```

### Loading Environment Variables
Use a library like `dotenv` to load environment variables:

```javascript
// Early in your application bootstrap
import dotenv from 'dotenv';
import path from 'path';

// Load environment-specific .env file
const envFile = `.env.${process.env.NODE_ENV || 'development'}`;
dotenv.config({ path: path.resolve(process.cwd(), envFile) });

// Fall back to default .env if specific one doesn't exist
dotenv.config({ path: path.resolve(process.cwd(), '.env') });
```

## Configuration Management

### Configuration Object
Create a centralized configuration object:

```javascript
// config.js
export default {
  server: {
    port: process.env.PORT || 8000,
    env: process.env.NODE_ENV || 'development',
    logLevel: process.env.LOG_LEVEL || 'info',
  },
  database: {
    host: process.env.DATABASE_HOST || 'localhost',
    port: parseInt(process.env.DATABASE_PORT || '5432', 10),
    name: process.env.DATABASE_NAME || 'app_dev',
    user: process.env.DATABASE_USER || 'postgres',
    password: process.env.DATABASE_PASSWORD || 'postgres',
  },
  security: {
    jwtSecret: process.env.JWT_SECRET || 'development_secret',
    jwtExpiration: process.env.JWT_EXPIRATION || '1d',
    corsOrigin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  },
};
```

### Configuration Validation
Validate configuration at startup:

```javascript
import Joi from 'joi';
import config from './config';

const configSchema = Joi.object({
  server: Joi.object({
    port: Joi.number().port().required(),
    env: Joi.string().valid('development', 'test', 'staging', 'production').required(),
    logLevel: Joi.string().valid('error', 'warn', 'info', 'debug').required(),
  }).required(),
  database: Joi.object({
    // Database validation
  }).required(),
  security: Joi.object({
    // Security validation
  }).required(),
});

const { error } = configSchema.validate(config);
if (error) {
  throw new Error(`Configuration validation error: ${error.message}`);
}
```

## Security Considerations

### Sensitive Information
- Never commit sensitive information to version control
- Use environment variables for secrets
- Consider using a secrets management service for production
- Rotate secrets regularly

### Environment-Specific Security
Adjust security settings based on environment:

```javascript
// security.js
import config from './config';

export const securityMiddleware = (app) => {
  // Apply security middleware based on environment
  if (config.server.env === 'production') {
    app.use(helmet()); // Strict security headers
    app.use(rateLimit({ /* strict limits */ }));
  } else if (config.server.env === 'staging') {
    app.use(helmet()); // Strict security headers
    app.use(rateLimit({ /* moderate limits */ }));
  } else {
    app.use(helmet({ contentSecurityPolicy: false })); // Relaxed for development
    // No rate limiting in development
  }
};
```

## Best Practices

1. **Fail Fast**: Validate configuration at startup
2. **Defaults**: Provide sensible defaults for all configuration values
3. **Documentation**: Document all environment variables and their purpose
4. **Isolation**: Keep environments completely isolated from each other
5. **Consistency**: Use the same configuration approach across all services
6. **Monitoring**: Log and alert on configuration issues
7. **Automation**: Automate environment setup and configuration
