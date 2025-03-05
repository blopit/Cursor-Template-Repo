# Port Standardization Guide

## Introduction

This guide outlines our standardized approach to port allocation for development environments. Consistent port usage across projects helps prevent conflicts, simplifies configuration, and improves developer experience.

## Why Standardize Ports?

- **Avoid Conflicts**: Prevent port collisions between different services
- **Simplify Configuration**: Reduce time spent configuring ports for each project
- **Improve Onboarding**: New team members can quickly understand and remember port assignments
- **Enhance Documentation**: Standardized ports make documentation more consistent
- **Streamline Debugging**: Easier to identify which service is running on which port

## Port Allocation Table

| Service Type | Application | Standard Port | Notes |
|--------------|-------------|---------------|-------|
| **Frontend** | React/Next.js | 3000 | Default Create React App port |
| | Vue.js | 3100 | |
| | Angular | 3200 | |
| | Static Site Generators | 3300 | Gatsby, Hugo, etc. |
| | Documentation Sites | 3400 | Storybook, Docusaurus, etc. |
| **Backend** | Primary API Server | 8000 | Django, Express, FastAPI, etc. |
| | Secondary API Server | 8001 | For microservices architecture |
| | GraphQL Server | 8080 | |
| | WebSocket Server | 8090 | |
| | Authentication Service | 8100 | |
| | File Upload Service | 8200 | |
| **Databases** | PostgreSQL | 5432 | Default PostgreSQL port |
| | MySQL/MariaDB | 3306 | Default MySQL port |
| | MongoDB | 27017 | Default MongoDB port |
| | Redis | 6379 | Default Redis port |
| | Elasticsearch | 9200 | Default Elasticsearch HTTP port |
| **DevOps** | Nginx/Reverse Proxy | 80, 443 | HTTP and HTTPS |
| | Adminer/Database UI | 8800 | |
| | Monitoring Tools | 9000 | Prometheus, Grafana, etc. |
| | CI/CD Services | 9100 | Jenkins, GitLab Runner, etc. |
| | Docker Registry | 5000 | |
| **Testing** | Test Runners | 9500 | Jest, Mocha, etc. |
| | Mock Servers | 9600 | |
| | Storybook | 6006 | Default Storybook port |
| | Cypress Dashboard | 9700 | |

## Implementation Guidelines

### Environment Variables

Always use environment variables for port configuration:

```dotenv
# Frontend
FRONTEND_PORT=3000

# Backend
API_PORT=8000
WEBSOCKET_PORT=8090

# Databases
DB_PORT=5432
REDIS_PORT=6379
```

### Docker Compose

When using Docker Compose, follow this pattern:

```yaml
services:
  frontend:
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
  
  backend:
    ports:
      - "${API_PORT:-8000}:8000"
  
  database:
    ports:
      - "${DB_PORT:-5432}:5432"
```

### Application Configuration

In your application code, always read port values from environment variables:

```javascript
// Node.js example
const port = process.env.API_PORT || 8000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

```python
# Python example
import os
port = int(os.getenv('API_PORT', 8000))
app.run(host='0.0.0.0', port=port)
```

## Port Conflict Resolution

If a port conflict occurs:

1. Run the port checker utility: `./tools/port_checker.sh`
2. Identify which service is using the conflicting port
3. Either:
   - Stop the conflicting service
   - Increment your port number by 1 (e.g., 3000 → 3001)
   - Configure your application to use a different port
4. Document any non-standard port usage in your project README

## Best Practices

1. **Document Port Usage**: Always include port information in your project README
2. **Use Environment Variables**: Never hardcode port numbers
3. **Check Port Availability**: Run the port checker before starting development
4. **Handle Port Binding Failures**: Implement proper error handling in your application
5. **Use Port Ranges**: For services that need multiple ports, use a consistent range
6. **Local Development Only**: These standards are for development environments only
7. **Production Environments**: In production, use standard ports (80/443) with proper routing

## Tools

We provide a port checker utility to help verify port availability:

```bash
# Check if common development ports are available
./tools/port_checker.sh
```

## Conclusion

Following these port standardization guidelines will help maintain consistency across projects and improve the development experience for all team members. If you have suggestions for improvements to this standard, please submit a pull request with your proposed changes. 