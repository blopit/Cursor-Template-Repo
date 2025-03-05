---
description: Documentation for the utility that checks port availability
globs: tools/port_checker.sh
---
# Port Checker Utility Documentation

## Purpose
The Port Checker Utility is a shell script that helps developers verify the availability of commonly used ports in the development environment. It checks predefined sets of ports for frontend applications, backend services, and databases, providing clear feedback on which ports are available or already in use.

## Usage
To use the Port Checker Utility:

```bash
# Check all predefined ports
./tools/port_checker.sh

# Check specific ports
./tools/port_checker.sh 3000 8000 5432

# Check with custom error message
./tools/port_checker.sh --message "Custom error message" 3000
```

The script will output:
- ✅ for ports that are available
- ❌ for ports that are in use
- A summary with suggestions for resolving port conflicts

## Dependencies
List of dependencies and relationships with other files/components:

- `.cursor/rules/port-standardization.mdc`: Defines the port allocation standards that this utility helps enforce
- Requires `nc` (netcat) to be installed on the system for port checking

## Maintenance
Guidelines for maintaining and updating this file:

- Update the predefined port lists when new standard ports are added
- Add support for additional port categories as needed
- Consider adding functionality to suggest alternative available ports
- Maintain compatibility with different operating systems (Linux, macOS, Windows with WSL)

## Additional Notes

### Port Categories
The utility checks the following port categories:

1. **Frontend Ports**: 3000, 3100, 3200, 3300, 3400
   - Commonly used by React, Next.js, Vue, and other frontend frameworks

2. **Backend Ports**: 8000, 8001, 8080, 8090, 8100, 8200
   - Used by FastAPI, Express, Django, and other backend services

3. **Database Ports**: 5432 (PostgreSQL), 3306 (MySQL), 27017 (MongoDB), 6379 (Redis), 9200 (Elasticsearch)
   - Standard ports for common database systems

### Integration Options
The port checker can be integrated into:
- Project setup scripts
- Development environment initialization
- Service startup scripts to provide early feedback on port conflicts
- CI/CD pipelines to verify port availability in test environments

### Future Enhancements
Potential improvements for future versions:
- Add support for checking remote hosts
- Implement automatic port selection for services
- Create a configuration file for customizing port lists
- Develop a companion utility for releasing ports 
