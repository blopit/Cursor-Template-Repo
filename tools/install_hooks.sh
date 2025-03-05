#!/bin/bash

# Script to install Git hooks
# This script copies the hooks from tools/hooks to .git/hooks and makes them executable

echo "Installing Git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
cp tools/hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

echo "✅ Installed pre-commit hook"

echo "Done! Git hooks installed successfully." 