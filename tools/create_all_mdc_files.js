#!/usr/bin/env node

/**
 * Script to create MDC files for all existing files in the src directory
 * 
 * Usage: node create_all_mdc_files.js
 * 
 * This script follows the rules defined in .cursor/rules/src-file-rules.mdc
 */

// Documentation: .cursor/rules/tools/create-all-mdc-files.mdc

const fs = require('node:fs');
const path = require('node:path');
const { execSync } = require('node:child_process');

// Function to recursively get all files in a directory
function getAllFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath);

  for (const file of files) {
    // Skip .DS_Store files
    if (file === '.DS_Store') {
      continue;
    }
    
    const filePath = path.join(dirPath, file);
    if (fs.statSync(filePath).isDirectory()) {
      // Skip node_modules and .cursor directories
      if (file !== 'node_modules' && file !== '.cursor') {
        getAllFiles(filePath, arrayOfFiles);
      }
    } else {
      arrayOfFiles.push(filePath);
    }
  }

  return arrayOfFiles;
}

// Get all files in the src directory
const srcPath = path.join(process.cwd(), 'src');
const allFiles = getAllFiles(srcPath);

console.log(`Found ${allFiles.length} files in the src directory`);

// Create MDC files for each file
let createdCount = 0;
let skippedCount = 0;

for (const filePath of allFiles) {
  // Convert absolute path to relative path
  const relativePath = path.relative(process.cwd(), filePath);
  
  try {
    // Run the create_mdc_file.js script for each file
    execSync(`node ${path.join(process.cwd(), 'tools', 'create_mdc_file.js')} ${relativePath}`);
    createdCount++;
  } catch (error) {
    console.error(`Error creating MDC file for ${relativePath}: ${error.message}`);
    skippedCount++;
  }
}

console.log(`Created ${createdCount} MDC files`);
if (skippedCount > 0) {
  console.log(`Skipped ${skippedCount} files due to errors`);
} 