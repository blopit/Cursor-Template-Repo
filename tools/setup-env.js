/**
 * Environment Setup Script
 * 
 * This script helps developers set up their environment files correctly.
 * It creates environment files based on .env.example if they don't exist.
 * 
 * Documentation: .cursor/rules/environment-configuration-rules.mdc
 */

const fs = require('node:fs');
const path = require('node:path');
const readline = require('node:readline');

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Define environment files
const ENV_FILES = {
  example: '.env.example',
  dev: '.env.dev',
  test: '.env.test',
  production: '.env.production'
};

// Check if file exists
function fileExists(filePath) {
  try {
    return fs.statSync(filePath).isFile();
  } catch (error) {
    return false;
  }
}

// Read file content
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    console.error(`Error reading file ${filePath}: ${error.message}`);
    return null;
  }
}

// Write file content
function writeFile(filePath, content) {
  try {
    fs.writeFileSync(filePath, content, 'utf8');
    return true;
  } catch (error) {
    console.error(`Error writing file ${filePath}: ${error.message}`);
    return false;
  }
}

// Parse environment file content into key-value pairs
function parseEnvFile(content) {
  const result = {};
  
  if (!content) return result;
  
  const lines = content.split('\n');
  
  for (const line of lines) {
    // Skip comments and empty lines
    if (line.trim().startsWith('#') || line.trim() === '') continue;
    
    // Split by first equals sign
    const equalIndex = line.indexOf('=');
    if (equalIndex === -1) continue;
    
    const key = line.substring(0, equalIndex).trim();
    const value = line.substring(equalIndex + 1).trim();
    
    result[key] = value;
  }
  
  return result;
}

// Convert key-value pairs back to environment file content
function formatEnvFile(variables, comments = {}) {
  let result = '';
  let currentCategory = null;
  
  for (const [key, value] of Object.entries(variables)) {
    // Add category comment if available
    const category = getCategoryFromKey(key);
    
    if (category !== currentCategory) {
      currentCategory = category;
      
      if (result !== '') {
        result += '\n';
      }
      
      result += `# ${category}\n`;
    }
    
    // Add variable comment if available
    if (comments[key]) {
      result += `# ${comments[key]}\n`;
    }
    
    result += `${key}=${value}\n`;
  }
  
  return result;
}

// Get category from key based on naming conventions
function getCategoryFromKey(key) {
  if (key.includes('ENVIRONMENT') || key.includes('DEBUG') || key.includes('LOG_LEVEL')) {
    return 'Environment';
  }
  
  if (key.includes('DATABASE')) {
    return 'Database';
  }
  
  if (key.includes('REDIS')) {
    return 'Redis';
  }
  
  if (key.includes('HOST') || key.includes('PORT')) {
    return 'Server Configuration';
  }
  
  if (key.includes('FRONTEND')) {
    return 'CORS';
  }
  
  if (key.includes('WS')) {
    return 'WebSocket';
  }
  
  if (key.includes('API')) {
    return 'API Configuration';
  }
  
  if (key.includes('OPENAI')) {
    return 'OpenAI Configuration';
  }
  
  if (key.includes('ELEVENLABS')) {
    return 'ElevenLabs';
  }
  
  return 'Other';
}

// Extract comments from environment file
function extractComments(content) {
  const result = {};
  let currentKey = null;
  
  if (!content) return result;
  
  const lines = content.split('\n');
  
  for (const line of lines) {
    if (line.trim().startsWith('#')) {
      // This is a comment line
      const comment = line.trim().substring(1).trim();
      
      // Skip category comments
      if (getCategoryFromComment(comment)) continue;
      
      // Store comment for the next variable
      currentKey = comment;
    } else if (line.trim() !== '') {
      // This is a variable line
      const equalIndex = line.indexOf('=');
      if (equalIndex === -1) continue;
      
      const key = line.substring(0, equalIndex).trim();
      
      // Associate comment with this variable
      if (currentKey) {
        result[key] = currentKey;
        currentKey = null;
      }
    }
  }
  
  return result;
}

// Get category from comment
function getCategoryFromComment(comment) {
  const categories = [
    'Environment', 'Database', 'Redis', 'Server Configuration',
    'CORS', 'WebSocket', 'API Configuration', 'OpenAI Configuration',
    'ElevenLabs'
  ];
  
  for (const category of categories) {
    if (comment.toLowerCase() === category.toLowerCase()) {
      return category;
    }
  }
  
  return null;
}

// Ask user for input with default value
function askQuestion(question, defaultValue) {
  return new Promise((resolve) => {
    rl.question(`${question} (${defaultValue}): `, (answer) => {
      resolve(answer.trim() || defaultValue);
    });
  });
}

// Main function
async function main() {
  console.log('Environment Setup Script');
  console.log('------------------------');
  
  // Check if example file exists
  if (!fileExists(ENV_FILES.example)) {
    console.error(`Error: ${ENV_FILES.example} file not found.`);
    rl.close();
    return;
  }
  
  // Read example file
  const exampleContent = readFile(ENV_FILES.example);
  if (!exampleContent) {
    rl.close();
    return;
  }
  
  // Parse example file
  const exampleVariables = parseEnvFile(exampleContent);
  const comments = extractComments(exampleContent);
  
  // Ask which environment to set up
  const environment = await askQuestion(
    'Which environment do you want to set up? (dev, test, production)',
    'dev'
  );
  
  if (!['dev', 'test', 'production'].includes(environment)) {
    console.error(`Error: Invalid environment "${environment}".`);
    rl.close();
    return;
  }
  
  const envFile = ENV_FILES[environment];
  
  // Check if environment file already exists
  if (fileExists(envFile)) {
    const overwrite = await askQuestion(
      `${envFile} already exists. Do you want to overwrite it? (yes/no)`,
      'no'
    );
    
    if (overwrite.toLowerCase() !== 'yes') {
      console.log(`Setup cancelled. ${envFile} was not modified.`);
      rl.close();
      return;
    }
  }
  
  // Create new environment variables based on example
  const newVariables = { ...exampleVariables };
  
  // Set environment-specific values
  newVariables.ENVIRONMENT = environment;
  
  if (environment === 'production') {
    newVariables.DEBUG = 'false';
    newVariables.LOG_LEVEL = 'WARNING';
  } else if (environment === 'test') {
    newVariables.DEBUG = 'true';
    newVariables.LOG_LEVEL = 'DEBUG';
    // Use test database
    if (newVariables.DATABASE_URL) {
      newVariables.DATABASE_URL = newVariables.DATABASE_URL.replace('mcp_dev', `mcp_test`);
    }
  }
  
  // Ask for sensitive values
  console.log('\nPlease provide values for sensitive environment variables:');
  
  for (const [key, value] of Object.entries(newVariables)) {
    // Only ask for API keys and sensitive information
    if (
      key.includes('API_KEY') || 
      key.includes('SECRET') || 
      key.includes('PASSWORD') ||
      value.includes('your-') ||
      value.includes('your_')
    ) {
      newVariables[key] = await askQuestion(`Enter value for ${key}`, value);
    }
  }
  
  // Format and write new environment file
  const newContent = formatEnvFile(newVariables, comments);
  
  if (writeFile(envFile, newContent)) {
    console.log(`\n✅ Successfully created ${envFile}`);
  } else {
    console.error(`\n❌ Failed to create ${envFile}`);
  }
  
  rl.close();
}

// Run main function
main().catch((error) => {
  console.error(`Error: ${error.message}`);
  rl.close();
}); 