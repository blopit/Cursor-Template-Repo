/**
 * Environment Variable Validation Script
 * 
 * This script validates that all required environment variables are set
 * and follows the best practices outlined in .env.md
 * 
 * Documentation: .cursor/rules/environment-configuration-rules.mdc
 */

const fs = require('node:fs');
const path = require('node:path');
const dotenv = require('dotenv');

// Determine environment
const NODE_ENV = process.env.NODE_ENV || 'development';
const envFile = `.env.${NODE_ENV}`;

console.log(`Validating environment variables for ${NODE_ENV} environment...`);

// Load environment variables
try {
  const result = dotenv.config({ path: envFile });
  
  if (result.error) {
    console.error(`Error loading ${envFile}: ${result.error.message}`);
    process.exit(1);
  }
  
  console.log(`Loaded environment from ${envFile}`);
} catch (error) {
  console.error(`Failed to load ${envFile}: ${error.message}`);
  process.exit(1);
}

// Define required variables by category
const requiredVariables = {
  environment: ['ENVIRONMENT', 'DEBUG', 'LOG_LEVEL'],
  database: ['DATABASE_URL'],
  redis: ['REDIS_URL'], // Or individual REDIS_HOST, REDIS_PORT, REDIS_DB
  server: ['HOST', 'PORT'],
  api: ['API_KEY'],
  cors: ['FRONTEND_URL'],
  websocket: ['WS_URL']
};

// Optional variables that might be required based on configuration
const conditionalVariables = {
  openai: ['OPENAI_API_KEY'],
  elevenlabs: ['ELEVENLABS_API_KEY', 'ELEVENLABS_VOICE_ID']
};

// Validate required variables
const missingVariables = [];

for (const [category, variables] of Object.entries(requiredVariables)) {
  console.log(`\nValidating ${category} variables...`);
  
  for (const variable of variables) {
    if (!process.env[variable]) {
      missingVariables.push(variable);
      console.error(`❌ Missing required variable: ${variable}`);
    } else {
      console.log(`✅ ${variable} is set`);
    }
  }
}

// Validate conditional variables
for (const [category, variables] of Object.entries(conditionalVariables)) {
  console.log(`\nValidating ${category} variables (if used)...`);
  
  for (const variable of variables) {
    if (!process.env[variable]) {
      console.warn(`⚠️ Optional variable not set: ${variable}`);
    } else {
      console.log(`✅ ${variable} is set`);
    }
  }
}

// Check for naming convention consistency (uppercase)
const allEnvVars = Object.keys(process.env);
const nonUppercaseVars = allEnvVars.filter(key => 
  // Only check our application variables, not system ones
  key.startsWith('APP_') || 
  key.startsWith('DB_') || 
  key.startsWith('REDIS_') || 
  key.startsWith('API_') ||
  requiredVariables.environment.includes(key) ||
  requiredVariables.database.includes(key) ||
  requiredVariables.server.includes(key) ||
  requiredVariables.cors.includes(key) ||
  requiredVariables.websocket.includes(key)
).filter(key => key !== key.toUpperCase());

if (nonUppercaseVars.length > 0) {
  console.log('\n⚠️ The following variables do not follow the uppercase naming convention:');
  for (const variable of nonUppercaseVars) {
    console.log(`  - ${variable} (should be ${variable.toUpperCase()})`);
  }
}

// Check for sensitive information patterns in values
const sensitivePatterns = [
  { name: 'API Key', pattern: /^(sk|pk)[-_][a-zA-Z0-9]{20,}$/ },
  { name: 'Password in URL', pattern: /[a-zA-Z0-9_-]+:[a-zA-Z0-9_-]+@/ }
];

console.log('\nChecking for potentially sensitive information...');
let hasSensitiveInfo = false;

for (const [key, value] of Object.entries(process.env)) {
  if (typeof value === 'string') {
    for (const { name, pattern } of sensitivePatterns) {
      if (pattern.test(value)) {
        console.warn(`⚠️ ${key} may contain sensitive information (${name})`);
        hasSensitiveInfo = true;
      }
    }
  }
}

if (!hasSensitiveInfo) {
  console.log('✅ No obvious sensitive information patterns detected');
}

// Final validation result
console.log('\n--- Validation Summary ---');

if (missingVariables.length > 0) {
  console.error(`❌ Missing ${missingVariables.length} required variables`);
  console.error('Please set the following variables in your environment:');
  for (const variable of missingVariables) {
    console.error(`  - ${variable}`);
  }
  process.exit(1);
} else {
  console.log('✅ All required environment variables are set');
  
  if (nonUppercaseVars.length > 0 || hasSensitiveInfo) {
    console.warn('⚠️ There are warnings you should address');
    process.exit(0);
  } else {
    console.log('✅ Environment configuration follows best practices');
    process.exit(0);
  }
} 