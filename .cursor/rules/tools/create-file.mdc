---
description: Documentation for the utility that creates files with proper formatting and MDC documentation
globs: tools/create_file.py
---
# File Creator Utility Documentation

## Purpose
The File Creator Utility is a tool that helps developers create new files following the project's file creation standards, automatically generating both the source file with proper formatting and its corresponding MDC documentation.

## Usage
Examples of how to use the File Creator Utility:

```bash
# Create a React component
python tools/create_file.py src/components/UserProfile --type tsx --description "User profile component that displays user information" --author "Your Name"

# Create a Python module
python tools/create_file.py src/utils/data_processor --type py --description "Utility for processing data"

# Create a CSS file
python tools/create_file.py src/styles/button --type css --description "Styles for button components"
```

## Dependencies
List of dependencies and relationships with other files/components:

- `.cursor/rules/file-creation-standards.mdc`: Defines the standards that this utility helps enforce
- Python standard library (os, sys, argparse, datetime, getpass)

## Maintenance
Guidelines for maintaining and updating this file:

- When adding support for new file types, update both the `TEMPLATES` dictionary and the argument parser choices
- Keep templates aligned with the latest coding standards for each language
- Update MDC template if the required documentation structure changes
- Consider adding validation for file paths to prevent overwriting existing files

## Additional Notes

### Supported File Types
The utility currently supports the following file types:
- JavaScript (js)
- React JSX (jsx)
- TypeScript (ts)
- React TSX (tsx)
- Python (py)
- CSS (css)
- SCSS (scss)
- Markdown (md)

### Directory Structure
The utility automatically creates the necessary directories for both the source file and the MDC documentation file. The MDC files are organized in subdirectories under `.cursor/rules/` based on the file type:

- JavaScript files: `.cursor/rules/javascript/`
- React components: `.cursor/rules/components/`
- TypeScript files: `.cursor/rules/typescript/`
- Python files: `.cursor/rules/python/`
- Style files: `.cursor/rules/styles/`
- Markdown files: `.cursor/rules/markdown/`

### Future Enhancements
Potential improvements for future versions:
- Add support for more file types (HTML, JSON, YAML, etc.)
- Implement a pre-commit hook to verify that new files have corresponding MDC documentation
- Add a validation mode to check existing files for compliance
- Create a GUI interface for easier file creation 
