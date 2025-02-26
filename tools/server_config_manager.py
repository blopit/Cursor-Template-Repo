#!/usr/bin/env python3
"""
Server Configuration Manager

This utility loads and manages MCP server configurations from YAML files.
It provides functions to get server configurations for different environments
and validate the configurations.
"""

import os
import yaml
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ServerConfigManager:
    """Manages MCP server configurations."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the server configuration manager.
        
        Args:
            config_path: Path to the server configuration file.
                         If None, uses the default path.
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config",
            "mcp_servers.yaml"
        )
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Load the server configuration from the YAML file.
        
        Returns:
            Dict containing the server configurations.
        
        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the YAML file is invalid.
        """
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded server configuration from {self.config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"Server configuration file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in server configuration: {e}")
            raise
    
    def get_environments(self) -> List[str]:
        """
        Get a list of available environments.
        
        Returns:
            List of environment names.
        """
        return list(self.config.get('environments', {}).keys())
    
    def get_servers(self, environment: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all server configurations for a specific environment.
        
        Args:
            environment: The environment name (e.g., 'development', 'production').
        
        Returns:
            Dict of server configurations for the specified environment.
            
        Raises:
            ValueError: If the environment doesn't exist.
        """
        if environment not in self.get_environments():
            raise ValueError(f"Environment '{environment}' not found in configuration")
        
        return self.config.get('environments', {}).get(environment, {}).get('servers', {})
    
    def get_server_config(self, environment: str, server_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific server in an environment.
        
        Args:
            environment: The environment name (e.g., 'development', 'production').
            server_name: The name of the server (e.g., 'main', 'analytics').
        
        Returns:
            Dict containing the server configuration with defaults applied.
            
        Raises:
            ValueError: If the environment or server doesn't exist.
        """
        servers = self.get_servers(environment)
        if server_name not in servers:
            raise ValueError(f"Server '{server_name}' not found in environment '{environment}'")
        
        # Get default configuration
        default_config = self.config.get('default', {})
        
        # Merge with server-specific configuration (server config takes precedence)
        server_config = servers[server_name]
        merged_config = {**default_config, **server_config}
        
        # Handle middleware separately to allow proper merging
        if 'middleware' in default_config and 'middleware' in server_config:
            # For now, just use the server's middleware if specified
            # A more sophisticated merge could be implemented if needed
            pass
        
        return merged_config
    
    def validate_config(self, environment: str, server_name: str) -> List[str]:
        """
        Validate a server configuration.
        
        Args:
            environment: The environment name.
            server_name: The name of the server.
        
        Returns:
            List of validation errors. Empty list if valid.
        """
        errors = []
        try:
            config = self.get_server_config(environment, server_name)
            
            # Check required fields
            required_fields = ['host', 'port', 'workers', 'timeout']
            for field in required_fields:
                if field not in config:
                    errors.append(f"Missing required field: {field}")
            
            # Validate SSL configuration
            if config.get('ssl_enabled', False):
                if 'ssl_cert' not in config:
                    errors.append("SSL enabled but ssl_cert not specified")
                if 'ssl_key' not in config:
                    errors.append("SSL enabled but ssl_key not specified")
            
            # Validate port range
            port = config.get('port')
            if port is not None and (port < 1 or port > 65535):
                errors.append(f"Invalid port number: {port}")
            
            # Validate workers
            workers = config.get('workers')
            if workers is not None and workers < 1:
                errors.append(f"Invalid number of workers: {workers}")
            
            # Validate timeout
            timeout = config.get('timeout')
            if timeout is not None and timeout < 1:
                errors.append(f"Invalid timeout: {timeout}")
            
        except ValueError as e:
            errors.append(str(e))
        
        return errors
    
    def save_config(self, config: Dict[str, Any], backup: bool = True) -> None:
        """
        Save the configuration to the YAML file.
        
        Args:
            config: The configuration to save.
            backup: Whether to create a backup of the existing file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        if backup and os.path.exists(self.config_path):
            backup_path = f"{self.config_path}.bak"
            try:
                with open(self.config_path, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
                logger.info(f"Created backup of server configuration at {backup_path}")
            except IOError as e:
                logger.error(f"Failed to create backup: {e}")
                raise
        
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            logger.info(f"Saved server configuration to {self.config_path}")
        except IOError as e:
            logger.error(f"Failed to save server configuration: {e}")
            raise

def get_server_config(environment: str, server_name: str = 'main') -> Dict[str, Any]:
    """
    Convenience function to get a server configuration.
    
    Args:
        environment: The environment name.
        server_name: The name of the server (defaults to 'main').
    
    Returns:
        Dict containing the server configuration.
    """
    manager = ServerConfigManager()
    return manager.get_server_config(environment, server_name)

def validate_server_config(environment: str, server_name: str = 'main') -> List[str]:
    """
    Convenience function to validate a server configuration.
    
    Args:
        environment: The environment name.
        server_name: The name of the server (defaults to 'main').
    
    Returns:
        List of validation errors. Empty list if valid.
    """
    manager = ServerConfigManager()
    return manager.validate_config(environment, server_name)

if __name__ == "__main__":
    import argparse
    import sys
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MCP Server Configuration Manager')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List environments command
    list_env_parser = subparsers.add_parser('list-environments', help='List available environments')
    
    # List servers command
    list_servers_parser = subparsers.add_parser('list-servers', help='List servers in an environment')
    list_servers_parser.add_argument('environment', help='Environment name')
    
    # Get server config command
    get_config_parser = subparsers.add_parser('get-config', help='Get server configuration')
    get_config_parser.add_argument('environment', help='Environment name')
    get_config_parser.add_argument('server', help='Server name', default='main', nargs='?')
    
    # Validate server config command
    validate_parser = subparsers.add_parser('validate', help='Validate server configuration')
    validate_parser.add_argument('environment', help='Environment name')
    validate_parser.add_argument('server', help='Server name', default='main', nargs='?')
    
    args = parser.parse_args()
    
    try:
        manager = ServerConfigManager()
        
        if args.command == 'list-environments':
            environments = manager.get_environments()
            print("Available environments:")
            for env in environments:
                print(f"  - {env}")
        
        elif args.command == 'list-servers':
            servers = manager.get_servers(args.environment)
            print(f"Servers in environment '{args.environment}':")
            for server_name in servers:
                print(f"  - {server_name}")
        
        elif args.command == 'get-config':
            config = manager.get_server_config(args.environment, args.server)
            print(f"Configuration for server '{args.server}' in environment '{args.environment}':")
            print(yaml.dump(config, default_flow_style=False))
        
        elif args.command == 'validate':
            errors = manager.validate_config(args.environment, args.server)
            if errors:
                print(f"Validation errors for server '{args.server}' in environment '{args.environment}':")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            else:
                print(f"Server '{args.server}' in environment '{args.environment}' has a valid configuration.")
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1) 