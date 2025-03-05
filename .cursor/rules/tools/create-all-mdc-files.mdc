# Create All MDC Files Tool Documentation

## Purpose
This tool automates the creation of MDC documentation files for all existing files in the src directory. It helps ensure that every source file has corresponding documentation, maintaining project standards and improving code maintainability.

## Usage
Run the script from the project root directory:
```bash
node tools/create_all_mdc_files.js
```

The script will:
1. Recursively scan the src directory for all files
2. Skip node_modules and .cursor directories
3. Create an MDC file for each source file using the create_mdc_file.js tool
4. Report the number of files created and any errors encountered

## Dependencies
- Node.js file system module (fs)
- Node.js path module (path)
- Node.js child_process module (execSync)
- create_mdc_file.js tool for individual MDC file creation

## Maintenance
When updating this tool, consider:
- Adding support for additional directories beyond src
- Implementing filters for specific file types
- Adding options for customizing MDC file templates
- Improving error handling and reporting

## Additional Notes
This tool is part of the project's documentation automation system, ensuring that all source files have corresponding MDC documentation files that follow the project's standards. 