# MCP Server Configuration

This document describes how to configure and manage MCP servers using the server configuration system.

## Overview

The MCP server configuration system allows you to define server configurations for different environments in a centralized YAML file. This makes it easy to manage multiple server configurations across different environments (development, test, staging, production) and ensures consistency in server setup.

## Configuration File

Server configurations are defined in `config/mcp_servers.yaml`. This file contains:

1. **Default configuration**: Applied to all servers unless overridden
2. **Environment-specific configurations**: Settings for each environment
3. **Server-specific configurations**: Settings for individual servers within each environment

### Example Configuration

```yaml
# Default configuration that applies to all servers unless overridden
default:
  workers: 4
  timeout: 30
  ssl_enabled: false
  log_level: "INFO"
  middleware:
    - SecurityMiddleware:
        enabled: true
    - MetricsMiddleware:
        enabled: true
        metrics_path: "/metrics"

# Environment-specific server configurations
environments:
  development:
    servers:
      main:
        host: "localhost"
        port: 8000
        workers: 2
        ssl_enabled: false
        log_level: "DEBUG"
        debug: true
      secondary:
        host: "localhost"
        port: 8001
        workers: 1
        ssl_enabled: false
        debug: true
  
  # Other environments...
```

## Configuration Structure

### Default Configuration

The `default` section contains settings that apply to all servers unless overridden by environment-specific or server-specific settings. Common defaults include:

- `workers`: Number of worker processes
- `timeout`: Request timeout in seconds
- `ssl_enabled`: Whether SSL is enabled
- `log_level`: Logging level
- `middleware`: List of middleware to apply

### Environment-Specific Configuration

Each environment (development, test, staging, production) has its own section under `environments`. Within each environment, there's a `servers` section that contains configurations for individual servers.

### Server-Specific Configuration

Each server within an environment has its own configuration. Server-specific settings override default settings. Common server settings include:

- `host`: Server hostname or IP address
- `port`: Server port
- `workers`: Number of worker processes
- `timeout`: Request timeout in seconds
- `ssl_enabled`: Whether SSL is enabled
- `ssl_cert`: Path to SSL certificate (if SSL is enabled)
- `ssl_key`: Path to SSL private key (if SSL is enabled)
- `log_level`: Logging level
- `debug`: Whether debug mode is enabled
- `middleware`: List of middleware to apply

## Using the Configuration

### Server Configuration Manager

The `ServerConfigManager` class in `tools/server_config_manager.py` provides methods to load, validate, and manage server configurations:

```python
from tools.server_config_manager import ServerConfigManager

# Create a manager instance
manager = ServerConfigManager()

# Get all environments
environments = manager.get_environments()

# Get all servers in an environment
servers = manager.get_servers('development')

# Get configuration for a specific server
config = manager.get_server_config('development', 'main')

# Validate a server configuration
errors = manager.validate_config('development', 'main')
```

### Convenience Functions

For common operations, you can use the convenience functions:

```python
from tools.server_config_manager import get_server_config, validate_server_config

# Get configuration for a server
config = get_server_config('development', 'main')

# Validate a server configuration
errors = validate_server_config('development', 'main')
```

## Command-Line Interface

The server configuration manager includes a command-line interface for common operations:

```bash
# List available environments
python tools/server_config_manager.py list-environments

# List servers in an environment
python tools/server_config_manager.py list-servers development

# Get configuration for a server
python tools/server_config_manager.py get-config development main

# Validate a server configuration
python tools/server_config_manager.py validate development main
```

## Example Usage

See `examples/mcp_server_example.py` for an example of how to use the server configuration with an MCP server:

```bash
# Run the example with default settings (development environment, main server)
python examples/mcp_server_example.py

# Run the example with a specific environment and server
python examples/mcp_server_example.py --env production --server analytics
```

## Best Practices

1. **Environment Isolation**: Keep configurations for different environments separate and appropriate for their context.
2. **Security**: Use environment variables for sensitive data like SSL keys and passwords.
3. **Validation**: Always validate configurations before using them.
4. **Documentation**: Document any custom settings or requirements for specific servers.
5. **Version Control**: Keep the configuration file in version control, but use environment variables for sensitive data.

## Troubleshooting

### Common Issues

1. **Configuration Not Found**: Ensure the configuration file exists at `config/mcp_servers.yaml`.
2. **Invalid Configuration**: Use the validation tools to check for configuration errors.
3. **Missing Required Fields**: Ensure all required fields (host, port, workers, timeout) are specified.
4. **SSL Configuration**: If SSL is enabled, ensure ssl_cert and ssl_key are specified.

### Debugging

Enable debug logging to see more information about the configuration loading process:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Extending the Configuration

To add new configuration options:

1. Update the YAML file with the new options
2. Update the validation logic in `ServerConfigManager.validate_config()`
3. Update the documentation to reflect the new options

## Security Considerations

1. **SSL Configuration**: Always enable SSL in production environments.
2. **Sensitive Data**: Use environment variables for sensitive data like SSL keys and passwords.
3. **Access Control**: Restrict access to the configuration file to authorized users.
4. **Validation**: Always validate configurations before using them to prevent security issues. 