#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

def run_command(cmd: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        return subprocess.run(cmd, capture_output=capture_output, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}", file=sys.stderr)
        print(f"STDOUT: {e.stdout}", file=sys.stderr)
        print(f"STDERR: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def get_changed_files() -> List[str]:
    """Get list of changed files."""
    result = run_command(['git', 'status', '--porcelain'])
    return [line[3:] for line in result.stdout.splitlines() if line]

def get_branch_name() -> str:
    """Get current branch name."""
    result = run_command(['git', 'branch', '--show-current'])
    return result.stdout.strip()

def create_commit_message(files: List[str], message: str) -> str:
    """Create a standardized commit message."""
    # Determine commit type based on files changed
    commit_type = "chore"
    if any(f.startswith('test') for f in files):
        commit_type = "test"
    elif any(f.endswith('.md') for f in files):
        commit_type = "docs"
    elif any(f.startswith('tools/') for f in files):
        commit_type = "feat"
    
    # Create commit message
    commit_msg = f"[Cursor] {commit_type}: {message}\n\nChanged files:\n"
    for file in files:
        commit_msg += f"- {file}\n"
    
    return commit_msg

def commit_changes(message: str, files: Optional[List[str]] = None) -> None:
    """Commit changes with a standardized message."""
    if files is None:
        files = get_changed_files()
    
    if not files:
        print("No changes to commit")
        return
    
    # Create commit message
    commit_msg = create_commit_message(files, message)
    
    # Write commit message to temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(commit_msg)
        temp_file = f.name
    
    try:
        # Add files
        run_command(['git', 'add'] + files)
        
        # Commit with message from file
        run_command(['git', 'commit', '-F', temp_file])
        
        print(f"Successfully committed changes:\n{commit_msg}")
    finally:
        # Clean up temporary file
        os.unlink(temp_file)

def create_pr(title: str, body: str, base_branch: str = "main") -> None:
    """Create a pull request using gh cli."""
    # Check if gh cli is installed
    try:
        run_command(['gh', '--version'])
    except subprocess.CalledProcessError:
        print("GitHub CLI (gh) is not installed. Please install it first.", file=sys.stderr)
        sys.exit(1)
    
    # Create PR
    current_branch = get_branch_name()
    pr_title = f"[Cursor] {title}"
    
    # Write PR body to temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(body)
        temp_file = f.name
    
    try:
        run_command([
            'gh', 'pr', 'create',
            '--title', pr_title,
            '--body-file', temp_file,
            '--base', base_branch
        ])
        print(f"Successfully created PR: {pr_title}")
    finally:
        # Clean up temporary file
        os.unlink(temp_file)

def create_feature_branch(feature_name: str) -> None:
    """Create a new feature branch."""
    # Sanitize feature name for branch
    branch_name = f"feature/{feature_name.lower().replace(' ', '-')}"
    
    # Create and checkout branch
    run_command(['git', 'checkout', '-b', branch_name])
    print(f"Created and switched to branch: {branch_name}")

def main():
    parser = argparse.ArgumentParser(description="Git automation tools")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Commit changes')
    commit_parser.add_argument('message', help='Commit message')
    commit_parser.add_argument('--files', nargs='+', help='Specific files to commit')
    
    # PR command
    pr_parser = subparsers.add_parser('pr', help='Create a pull request')
    pr_parser.add_argument('title', help='PR title')
    pr_parser.add_argument('body', help='PR description')
    pr_parser.add_argument('--base', default='main', help='Base branch')
    
    # Feature branch command
    feature_parser = subparsers.add_parser('feature', help='Create a feature branch')
    feature_parser.add_argument('name', help='Feature name')
    
    args = parser.parse_args()
    
    if args.command == 'commit':
        commit_changes(args.message, args.files)
    elif args.command == 'pr':
        create_pr(args.title, args.body, args.base)
    elif args.command == 'feature':
        create_feature_branch(args.name)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main() 