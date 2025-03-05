---
description: Documentation for the pre-commit hook that enforces MDC documentation requirements
globs: *.git/hooks/pre-commit,tools/hooks/pre-commit
---
# Pre-Commit Hook Documentation

## Purpose
The pre-commit hook enforces the MDC documentation requirement by checking that new files have corresponding MDC documentation files before allowing commits.

## Usage
The pre-commit hook is automatically executed when you run `git commit`. It checks all staged files to ensure they have corresponding MDC documentation.

To install the hook:
```bash
# Run the installation script
./tools/install_hooks.sh
```

If the hook blocks your commit due to missing MDC documentation:
```bash
# Create the missing MDC file(s) using the file creation utility
./tools/create_file.py path/to/your/file --type file_type --description "Description"

# Or manually create the MDC file following the template in file-creation-standards.mdc

# Then try committing again
git commit
```

To bypass the hook (not recommended):
```bash
git commit --no-verify
```

## Dependencies
List of dependencies and relationships with other files/components:

- `.cursor/rules/file-creation-standards.mdc`: Defines the standards that this hook enforces
- `tools/create_file.py`: Utility for creating files with proper MDC documentation
- `tools/install_hooks.sh`: Script to install the hook

## Maintenance
Guidelines for maintaining and updating this file:

- Update the directories and file extensions to check as the project evolves
- Add new exceptions as needed for files that don't require MDC documentation
- Improve error messages to be more helpful
- Consider adding more sophisticated checks for MDC content quality

## Additional Notes

### How It Works
The hook performs the following checks:
1. Gets a list of all staged files
2. Filters files based on directory, extension, and exceptions
3. Checks if each file contains a reference to an MDC documentation file
4. Verifies that the referenced MDC file actually exists
5. Blocks the commit if any files are missing MDC documentation

### Customization
You can customize the hook by modifying:
- `src_dirs`: Directories to check for files requiring MDC documentation
- `extensions`: File extensions that require MDC documentation
- `exceptions`: Files that are exempt from the MDC documentation requirement 
