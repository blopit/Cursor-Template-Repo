import os
import shutil
import argparse
from pathlib import Path
from typing import Optional

def backup_env(env_path: Path, backup_suffix: str = 'backup') -> Optional[Path]:
    """Backup existing .env file if it exists."""
    if env_path.exists():
        backup_path = env_path.with_suffix(f'.{backup_suffix}')
        shutil.copy2(env_path, backup_path)
        return backup_path
    return None

def switch_environment(env_type: str) -> None:
    """Switch to a different environment configuration."""
    root_dir = Path.cwd()
    env_path = root_dir / '.env'
    target_env = root_dir / f'.env.{env_type}'
    
    if not target_env.exists():
        raise FileNotFoundError(f"Environment file .env.{env_type} not found")
    
    # Create backup of current .env if it exists
    if env_path.exists():
        backup_path = backup_env(env_path)
        print(f"Backed up current .env to {backup_path}")
    
    # Create symlink to target environment
    if os.name == 'nt':  # Windows
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Warning: On Windows, you may need admin privileges to create symlinks")
        os.system(f'mklink {env_path} {target_env}')
    else:  # Unix-like
        if env_path.exists():
            env_path.unlink()
        env_path.symlink_to(target_env)
    
    print(f"Switched to {env_type} environment")

def list_environments() -> None:
    """List all available environment configurations."""
    root_dir = Path.cwd()
    env_files = list(root_dir.glob('.env.*'))
    
    if not env_files:
        print("No environment configurations found")
        return
    
    print("\nAvailable environments:")
    for env_file in env_files:
        env_type = env_file.suffix[1:]  # Remove the leading dot
        if env_type != 'backup':
            print(f"- {env_type}")
    
    current_env = root_dir / '.env'
    if current_env.exists() and current_env.is_symlink():
        current = current_env.resolve().name.replace('.env.', '')
        print(f"\nCurrent environment: {current}")
    else:
        print("\nCurrent environment: not linked to any environment file")

def main():
    parser = argparse.ArgumentParser(description='Manage environment configurations')
    parser.add_argument('action', choices=['switch', 'list'], help='Action to perform')
    parser.add_argument('--env', help='Environment to switch to (e.g., dev, prod)')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'list':
            list_environments()
        elif args.action == 'switch':
            if not args.env:
                parser.error("--env is required when using 'switch'")
            switch_environment(args.env)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 