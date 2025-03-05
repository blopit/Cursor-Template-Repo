#!/usr/bin/env node

/**
 * Script to create MDC files for source files
 * 
 * Usage: node create_mdc_file.js <path_to_source_file>
 * Example: node create_mdc_file.js src/frontend/components/Button.js
 * 
 * This script follows the rules defined in .cursor/rules/src-file-rules.mdc
 */

// Documentation: .cursor/rules/tools/create-mdc-file.mdc

const fs = require('node:fs');
const path = require('node:path');

// Get the source file path from command line arguments
const sourceFilePath = process.argv[2];

if (!sourceFilePath) {
  console.error('Please provide a source file path');
  process.exit(1);
}

// Check if the file is in the src directory
if (!sourceFilePath.startsWith('src/')) {
  console.error('The file must be in the src directory');
  process.exit(1);
}

// Get the file name and extension
const fileInfo = path.parse(sourceFilePath);
const fileName = fileInfo.name;
const fileExtension = fileInfo.ext;

// Create the corresponding MDC file path
const mdcFilePath = sourceFilePath
  .replace('src/', '.cursor/rules/src/')
  .replace(fileExtension, '.mdc');

// Create the directory structure if it doesn't exist
const mdcDirPath = path.dirname(mdcFilePath);
if (!fs.existsSync(mdcDirPath)) {
  fs.mkdirSync(mdcDirPath, { recursive: true });
  console.log(`Created directory: ${mdcDirPath}`);
}

// Create the MDC file content
const mdcContent = `# ${fileName} Guidelines

## Purpose
[Describe the purpose of the file]

## Usage Guidelines
[Explain how to use the code in this file]

## Dependencies
[List dependencies]

## Best Practices
- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

## Examples
\`\`\`${fileExtension.replace('.', '')}
[Example code]
\`\`\`
`;

// Write the MDC file
fs.writeFileSync(mdcFilePath, mdcContent);
console.log(`Created MDC file: ${mdcFilePath}`);

// Check if the source file exists
if (!fs.existsSync(sourceFilePath)) {
  console.warn(`Warning: The source file ${sourceFilePath} does not exist yet.`);
} 