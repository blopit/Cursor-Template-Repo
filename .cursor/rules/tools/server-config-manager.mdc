# Server Configuration Manager Documentation

## Purpose
The Server Configuration Manager is a utility for loading, validating, and managing MCP server configurations from YAML files. It provides a centralized way to handle server configurations across different environments (development, testing, production), ensuring consistent configuration management and validation.

## Usage
The module can be used both as a library and as a command-line tool:

### Library Usage
```python
# Get a server configuration
from tools.scripts.server_config_manager import get_server_config
config = get_server_config('production', 'main')

# Validate a server configuration
from tools.scripts.server_config_manager import validate_server_config
errors = validate_server_config('production', 'main')
if not errors:
    print("Configuration is valid")
else:
    print("Configuration errors:", errors)

# Use the ServerConfigManager class directly
from tools.scripts.server_config_manager import ServerConfigManager
manager = ServerConfigManager()
environments = manager.get_environments()
```

### Command-Line Usage
```bash
# List available environments
python tools/scripts/server_config_manager.py list-environments

# List servers in an environment
python tools/scripts/server_config_manager.py list-servers production

# Get server configuration
python tools/scripts/server_config_manager.py get-config production main

# Validate server configuration
python tools/scripts/server_config_manager.py validate-config production main
```

## Dependencies
- PyYAML: For parsing YAML configuration files
- Python standard libraries: os, logging, typing, pathlib, argparse, sys

## Maintenance
When updating this tool, consider:
- Adding support for additional configuration formats (JSON, TOML)
- Implementing more sophisticated validation rules
- Adding functionality to generate configuration templates
- Enhancing the command-line interface with additional commands
- Improving error handling and reporting

## Additional Notes
The tool follows the MCP server configuration standards and ensures that all server configurations have the required fields and valid values. It also provides backup functionality when saving configurations to prevent data loss. 