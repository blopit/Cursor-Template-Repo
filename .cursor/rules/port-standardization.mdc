---
description: Guidelines for standardizing port allocations and configuration practices
globs: *.js,*.ts,*.py,*.sh,docker-compose.yml,Dockerfile
---
# Port Standardization Guidelines

## Purpose
This document defines the standard port allocations and configuration practices for all services in the project. Following these guidelines ensures consistency, prevents port conflicts, and simplifies development and deployment processes.

## Port Allocation Standards

### Core Services
| Service Type | Port Range | Default Port | Notes |
|--------------|------------|--------------|-------|
| Frontend Applications | 3000-3999 | 3000 | React, Next.js, Vue applications |
| Backend APIs | 8000-8999 | 8000 | FastAPI, Express, Django services |
| Database Services | 5000-5999 | 5432 | PostgreSQL default is 5432 |
| Cache Services | 6000-6999 | 6379 | Redis default is 6379 |
| Message Queues | 7000-7999 | 7000 | RabbitMQ, Kafka services |

### Development Environment
- Frontend applications should use port 3000 by default
- Backend services should use port 8000 by default
- Each developer should increment by 1 when running multiple instances
  - Example: First frontend on 3000, second on 3001, etc.

### Testing Environment
- Test services should use the same port as development
- Automated tests should use dynamic ports or dedicated test ports
- CI/CD pipelines should use configurable ports to prevent conflicts

### Production Environment
- Production services should use standard ports (80/443)
- Internal services should follow the same numbering scheme behind a reverse proxy
- All port configurations must be environment-variable driven

## Configuration Guidelines

### Environment Variables
- Use `PORT` for the main application port
- Use `SERVICE_NAME_PORT` for specific service ports
- Include port configurations in `.env.example`
- Document all port requirements in service README files

### Docker Configuration
- Expose internal ports using the same numbering scheme
- Map to host ports explicitly in docker-compose files
- Use environment variables for port configuration
- Document port mappings in service documentation

### Conflict Resolution
- Automated port conflict detection should be implemented
- Services should attempt to use alternative ports when conflicts occur
- Clear error messages should be provided when ports are unavailable

## Implementation Tools

### Port Checker Utility
The project includes a port checker utility (`tools/port_checker.sh`) that:
- Verifies if required ports are available
- Suggests alternative ports when conflicts exist
- Can be integrated into service startup scripts

### Usage Example
```bash
# Check if the default frontend port is available
./tools/port_checker.sh 3000

# Check multiple ports
./tools/port_checker.sh 3000 8000 5432

# Check with custom error message
./tools/port_checker.sh --message "Custom frontend port unavailable" 3000
```

## Maintenance
- This document should be updated when new service types are added
- Port ranges should be reviewed quarterly to ensure they remain appropriate
- The port checker utility should be maintained to support new requirements
- Conflicts and resolutions should be documented for future reference

## Additional Notes
- Services should gracefully handle port conflicts with clear error messages
- Documentation for each service should include port requirements
- Local development tools should respect these port standards
- Consider implementing service discovery for more dynamic environments 
