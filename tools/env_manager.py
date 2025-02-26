#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

def validate_environment(env_type: str, env_vars: Dict[str, str]) -> List[str]:
    """
    Validate environment variables based on environment type.
    Returns a list of validation errors.
    """
    errors = []
    
    # Common required variables for all environments
    required_vars = [
        'APP_ENV', 'APP_NAME', 'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'
    ]
    
    # Check for missing required variables
    for var in required_vars:
        if var not in env_vars or not env_vars[var]:
            errors.append(f"Missing required environment variable: {var}")
    
    # Environment-specific validation
    if env_type == 'production':
        # Production-specific checks
        if env_vars.get('APP_DEBUG', '').lower() == 'true':
            errors.append("APP_DEBUG should be set to 'false' in production")
        
        if not env_vars.get('SSL_CERT_PATH'):
            errors.append("SSL_CERT_PATH is required in production")
            
        if not env_vars.get('SSL_KEY_PATH'):
            errors.append("SSL_KEY_PATH is required in production")
    
    elif env_type == 'test':
        # Test-specific checks
        if not env_vars.get('DB_NAME', '').endswith('_test'):
            errors.append("Test database name should end with '_test'")
    
    return errors

def parse_env_file(file_path: Path) -> Dict[str, str]:
    """Parse environment file and return variables as dictionary."""
    if not file_path.exists():
        return {}
    
    env_vars = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def backup_env(env_path: Path) -> Path:
    """Create a backup of the current environment file."""
    if not env_path.exists():
        return None
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = env_path.with_suffix(f".backup.{timestamp}")
    shutil.copy2(env_path, backup_path)
    return backup_path

def restore_env_backup(backup_path: Path) -> None:
    """Restore environment from a backup file."""
    env_path = Path.cwd() / '.env'
    
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file {backup_path} not found")
    
    shutil.copy2(backup_path, env_path)
    print(f"Restored environment from {backup_path}")

def list_env_backups() -> List[Path]:
    """List all environment backup files."""
    root_dir = Path.cwd()
    return sorted(root_dir.glob('.env.backup.*'))

def switch_environment(env_type: str) -> None:
    """Switch to a different environment configuration."""
    root_dir = Path.cwd()
    env_path = root_dir / '.env'
    target_env = root_dir / f'.env.{env_type}'
    
    if not target_env.exists():
        raise FileNotFoundError(f"Environment file .env.{env_type} not found")
    
    # Parse target environment to validate
    env_vars = parse_env_file(target_env)
    validation_errors = validate_environment(env_type, env_vars)
    
    if validation_errors:
        print(f"Validation errors in {target_env}:", file=sys.stderr)
        for error in validation_errors:
            print(f"  - {error}", file=sys.stderr)
        
        if input("Continue despite validation errors? (y/N): ").lower() != 'y':
            print("Environment switch aborted.")
            return
    
    # Create backup of current .env if it exists
    if env_path.exists():
        backup_path = backup_env(env_path)
        if backup_path:
            print(f"Backed up current .env to {backup_path}")
    
    # Copy the target environment file to .env
    shutil.copy2(target_env, env_path)
    print(f"Switched to {env_type} environment")
    
    # Print active environment variables
    print("\nActive environment variables:")
    for key, value in sorted(env_vars.items()):
        # Mask sensitive values
        if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key']):
            value = '*' * 8
        print(f"  {key}={value}")

def create_env_template() -> None:
    """Create a new .env.example template file."""
    root_dir = Path.cwd()
    template_path = root_dir / '.env.example'
    
    if template_path.exists():
        if input(f"{template_path} already exists. Overwrite? (y/N): ").lower() != 'y':
            print("Template creation aborted.")
            return
    
    with open(template_path, 'w') as f:
        f.write("""# Application Settings
APP_NAME=MyApp
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_db
DB_USER=db_user
DB_PASSWORD=db_password

# API Keys and External Services
API_KEY=your_api_key
EXTERNAL_SERVICE_URL=https://api.example.com

# Logging and Monitoring
LOG_LEVEL=info
ENABLE_METRICS=false
""")
    
    print(f"Created environment template at {template_path}")

def main():
    parser = argparse.ArgumentParser(description="Environment configuration manager")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Switch command
    switch_parser = subparsers.add_parser('switch', help='Switch to a different environment')
    switch_parser.add_argument('environment', choices=['development', 'test', 'production'], 
                              help='Target environment')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate environment configuration')
    validate_parser.add_argument('environment', nargs='?', 
                                help='Environment to validate (defaults to current .env)')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create a backup of the current environment')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from a backup')
    restore_parser.add_argument('backup', help='Backup file to restore from')
    
    # List backups command
    subparsers.add_parser('list-backups', help='List all environment backups')
    
    # Create template command
    subparsers.add_parser('create-template', help='Create a new .env.example template')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'switch':
            switch_environment(args.environment)
        elif args.command == 'validate':
            env_path = Path.cwd() / (f'.env.{args.environment}' if args.environment else '.env')
            if not env_path.exists():
                print(f"Environment file {env_path} not found", file=sys.stderr)
                sys.exit(1)
                
            env_vars = parse_env_file(env_path)
            env_type = args.environment or env_vars.get('APP_ENV', 'development')
            
            errors = validate_environment(env_type, env_vars)
            if errors:
                print(f"Validation errors in {env_path}:", file=sys.stderr)
                for error in errors:
                    print(f"  - {error}", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Environment configuration is valid for {env_type}")
        elif args.command == 'backup':
            env_path = Path.cwd() / '.env'
            if not env_path.exists():
                print("No .env file found to backup", file=sys.stderr)
                sys.exit(1)
                
            backup_path = backup_env(env_path)
            print(f"Created backup at {backup_path}")
        elif args.command == 'restore':
            backup_path = Path(args.backup)
            restore_env_backup(backup_path)
        elif args.command == 'list-backups':
            backups = list_env_backups()
            if not backups:
                print("No environment backups found")
            else:
                print("Available environment backups:")
                for i, backup in enumerate(backups, 1):
                    timestamp = backup.suffix.split('.')[-1]
                    print(f"  {i}. {backup.name} (created: {timestamp})")
        elif args.command == 'create-template':
            create_env_template()
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 