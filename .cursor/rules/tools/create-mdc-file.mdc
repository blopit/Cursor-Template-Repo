# Create MDC File Tool Documentation

## Purpose
This tool creates MDC (Markdown Cursor) documentation files for individual source files. It generates a standardized template for documenting file purpose, usage guidelines, dependencies, and best practices, ensuring consistent documentation across the project.

## Usage
Run the script from the project root directory with a path to the source file:
```bash
node tools/create_mdc_file.js <path_to_source_file>
```

Example:
```bash
node tools/create_mdc_file.js src/frontend/components/Button.js
```

The script will:
1. Verify the file is in the src directory
2. Create the corresponding MDC file path in the .cursor/rules/src directory
3. Generate a template MDC file with standard sections
4. Create any necessary directory structure

## Dependencies
- Node.js file system module (fs)
- Node.js path module (path)

## Maintenance
When updating this tool, consider:
- Enhancing the MDC template with additional sections
- Adding support for different file types with specialized templates
- Implementing options for custom templates
- Adding validation for existing MDC files

## Additional Notes
This tool is designed to work with the project's documentation standards as defined in .cursor/rules/src-file-rules.mdc. It helps maintain consistent documentation across the codebase and ensures that all source files have corresponding documentation. 