/**
 * Main Application Entry Point
 * 
 * This file demonstrates how to use the authentication services together.
 * It provides examples of user registration, login, and other authentication operations.
 */

const { AuthService } = require('./services/auth-service');
const { UserRepository } = require('./repositories/user-repository');
const { EmailService } = require('./services/email-service');
const { PasswordService } = require('./services/password-service');

// Create instances of the required services
const userRepository = new UserRepository();
const emailService = new EmailService();
const passwordService = new PasswordService();

// Create the authentication service
const authService = new AuthService(
  userRepository,
  emailService,
  passwordService
);

/**
 * Example: Register a new user
 */
async function registerUserExample() {
  try {
    // User data for registration
    const userData = {
      email: 'user@example.com',
      password: 'SecureP@ss123',
      firstName: 'John',
      lastName: 'Doe'
    };
    
    console.log('Registering user:', userData.email);
    
    // Register the user
    const result = await authService.registerUser(userData);
    
    console.log('Registration successful:', result);
    
    return result.user;
  } catch (error) {
    console.error('Registration failed:', error.message);
    return null;
  }
}

/**
 * Example: Register a user with invalid data
 */
async function registerInvalidUserExample() {
  try {
    // Invalid user data (missing required fields)
    const userData = {
      email: 'invalid-email',
      password: 'short',
      firstName: '',
      lastName: 'Doe'
    };
    
    console.log('Attempting to register with invalid data');
    
    // This should fail with validation errors
    const result = await authService.registerUser(userData);
    
    console.log('Registration result:', result);
    
    return result.user;
  } catch (error) {
    console.error('Registration failed as expected:', error.message);
    return null;
  }
}

/**
 * Example: Register a duplicate user
 */
async function registerDuplicateUserExample() {
  try {
    // User data for registration (same email as first example)
    const userData = {
      email: 'user@example.com', // Duplicate email
      password: 'AnotherP@ss456',
      firstName: 'Jane',
      lastName: 'Smith'
    };
    
    console.log('Attempting to register with duplicate email');
    
    // This should fail with duplicate email error
    const result = await authService.registerUser(userData);
    
    console.log('Registration result:', result);
    
    return result.user;
  } catch (error) {
    console.error('Registration failed as expected:', error.message);
    return null;
  }
}

/**
 * Run the examples
 */
async function runExamples() {
  console.log('=== User Registration Examples ===');
  
  // Register a valid user
  const user = await registerUserExample();
  
  // Try to register with invalid data
  await registerInvalidUserExample();
  
  // Try to register with a duplicate email
  await registerDuplicateUserExample();
  
  console.log('=== Examples Complete ===');
}

// Run the examples
runExamples().catch(error => {
  console.error('Error running examples:', error);
}); 