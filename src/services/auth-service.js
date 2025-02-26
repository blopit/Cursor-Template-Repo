/**
 * Authentication Service
 * 
 * This service handles user authentication operations including registration,
 * login, password management, and profile updates as specified in REQ-AUTH-001
 * and designed in DES-AUTH-001.
 */

class AuthService {
  /**
   * Creates a new AuthService instance
   * 
   * @param {Object} userRepository - Repository for user data operations
   * @param {Object} emailService - Service for sending emails
   * @param {Object} passwordService - Service for password hashing and verification
   */
  constructor(userRepository, emailService, passwordService) {
    this.userRepository = userRepository;
    this.emailService = emailService;
    this.passwordService = passwordService;
  }

  /**
   * Registers a new user with the provided data
   * 
   * @param {Object} userData - User registration data
   * @param {string} userData.email - User's email address
   * @param {string} userData.password - User's password
   * @param {string} userData.firstName - User's first name
   * @param {string} userData.lastName - User's last name
   * @returns {Promise<Object>} - Registration result with user data
   * @throws {Error} If registration fails due to validation or existing email
   */
  async registerUser(userData) {
    try {
      // Validate user data
      this.validateUserData(userData);
      
      // Check if email already exists
      const existingUser = await this.userRepository.findByEmail(userData.email);
      if (existingUser) {
        throw new Error('Email already registered');
      }
      
      // Hash the password
      const passwordHash = this.passwordService.hashPassword(userData.password);
      
      // Create user object
      const user = await this.userRepository.save({
        email: userData.email,
        passwordHash: passwordHash,
        firstName: userData.firstName,
        lastName: userData.lastName,
        isEmailVerified: false,
        failedLoginAttempts: 0
      });
      
      // Generate verification token and send email
      const verificationToken = this.generateVerificationToken();
      
      try {
        await this.emailService.sendVerificationEmail(userData.email, verificationToken);
        return {
          success: true,
          user,
          emailSent: true
        };
      } catch (emailError) {
        // Continue with registration even if email sending fails
        return {
          success: true,
          user,
          emailSent: false,
          emailError: `Failed to send verification email: ${emailError.message}`
        };
      }
    } catch (error) {
      // Handle repository errors
      if (error.message.includes('Database error')) {
        throw new Error(`Registration failed: ${error.message}`);
      }
      
      // Re-throw validation errors
      throw error;
    }
  }

  /**
   * Validates user registration data
   * 
   * @param {Object} userData - User data to validate
   * @throws {Error} If validation fails
   */
  validateUserData(userData) {
    // Validate email
    if (!userData.email) {
      throw new Error('Email is required');
    }
    
    if (!this.isValidEmail(userData.email)) {
      throw new Error('Invalid email format');
    }
    
    // Validate password
    if (!userData.password) {
      throw new Error('Password is required');
    }
    
    if (userData.password.length < 8) {
      throw new Error('Password must be at least 8 characters');
    }
    
    if (!this.isValidPassword(userData.password)) {
      throw new Error('Password must include at least one uppercase letter, one lowercase letter, one number, and one special character');
    }
    
    // Validate name
    if (!userData.firstName) {
      throw new Error('First name is required');
    }
    
    if (!userData.lastName) {
      throw new Error('Last name is required');
    }
  }

  /**
   * Validates email format
   * 
   * @param {string} email - Email to validate
   * @returns {boolean} True if email format is valid
   */
  isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  /**
   * Validates password complexity
   * 
   * @param {string} password - Password to validate
   * @returns {boolean} True if password meets complexity requirements
   */
  isValidPassword(password) {
    // Check for at least one uppercase letter
    const hasUppercase = /[A-Z]/.test(password);
    
    // Check for at least one lowercase letter
    const hasLowercase = /[a-z]/.test(password);
    
    // Check for at least one number
    const hasNumber = /[0-9]/.test(password);
    
    // Check for at least one special character
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
    
    return hasUppercase && hasLowercase && hasNumber && hasSpecial;
  }

  /**
   * Generates a verification token for email verification
   * 
   * @returns {string} Verification token
   */
  generateVerificationToken() {
    // Simple implementation for now
    return Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
  }
}

module.exports = { AuthService }; 