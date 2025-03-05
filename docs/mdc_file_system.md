# MDC File System

## Overview

The MDC (Markdown Cursor) file system is a set of rules and tools to ensure that every file in the `src` directory has a corresponding `.mdc` file in the `.cursor/rules/src` directory with the same relative path structure. These MDC files contain guidelines, best practices, and examples for working with the corresponding source files.

## Directory Structure

The directory structure in `.cursor/rules/src` mirrors the structure in `src`:
- `src/frontend` → `.cursor/rules/src/frontend`
- `src/backend` → `.cursor/rules/src/backend`
- Any subdirectories are also mirrored

The `.cursor/rules/src` directory should be a perfect mirror of the `src` directory, containing only MDC files that correspond to actual files in the `src` directory.

## MDC File Content

Each MDC file follows a standard template with the following sections:
1. **File Purpose**: A clear description of what the file does
2. **Usage Guidelines**: How to use the code in this file
3. **Dependencies**: What other files or modules this file depends on
4. **Best Practices**: Specific coding standards or patterns to follow
5. **Examples**: Example usage if applicable

## Automatic MDC File Creation

The system includes several tools to automate the creation of MDC files:

### 1. Pre-commit Hook

A Git pre-commit hook automatically creates MDC files for new files added to the `src` directory. When you stage a new file in the `src` directory and commit it, the hook will:
1. Create a corresponding MDC file in `.cursor/rules/src`
2. Add the MDC file to the staging area
3. Include it in the commit

The pre-commit hook is located at `.git/hooks/pre-commit`.

### 2. Manual MDC File Creation

You can manually create an MDC file for a specific source file using the `create_mdc_file.js` script:

```bash
node tools/create_mdc_file.js src/path/to/your/file.js
```

This will create a corresponding MDC file at `.cursor/rules/src/path/to/your/file.mdc`.

### 3. Bulk MDC File Creation

To create MDC files for all existing files in the `src` directory, you can use the `create_all_mdc_files.js` script:

```bash
node tools/create_all_mdc_files.js
```

This will scan the entire `src` directory and create MDC files for all files that don't already have one.

## Rules

The rules for the MDC file system are defined in `.cursor/rules/src-file-rules.mdc`. These rules specify:
1. The requirement for MDC files for every source file
2. The structure and content of MDC files
3. The directory structure mirroring between `src` and `.cursor/rules/src`

## Benefits

The MDC file system provides several benefits:
1. **Consistent Documentation**: Ensures every file has proper documentation
2. **Best Practices**: Provides guidelines for working with each file
3. **Examples**: Offers examples of how to use the code
4. **Onboarding**: Makes it easier for new developers to understand the codebase
5. **Maintenance**: Helps maintain code quality over time

## Troubleshooting

If you encounter issues with the MDC file system:
1. Check that the pre-commit hook is executable (`chmod +x .git/hooks/pre-commit`)
2. Ensure the scripts in the `tools` directory are executable
3. Run the `create_all_mdc_files.js` script to create any missing MDC files
4. Check the console output for any error messages 