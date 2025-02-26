/**
 * User Repository
 * 
 * This repository handles user data persistence operations as specified in DES-AUTH-001.
 * It provides methods for finding, saving, updating, and deleting user records.
 */

class UserRepository {
  /**
   * Creates a new UserRepository instance
   * 
   * @param {Object} database - Database connection or client
   */
  constructor(database) {
    this.database = database;
    this.users = []; // In-memory storage for simplicity, would use database in production
  }

  /**
   * Finds a user by ID
   * 
   * @param {string} id - User ID
   * @returns {Promise<Object|null>} User object or null if not found
   */
  async findById(id) {
    try {
      // In a real implementation, this would query the database
      return this.users.find(user => user.id === id) || null;
    } catch (error) {
      throw new Error(`Database error: ${error.message}`);
    }
  }

  /**
   * Finds a user by email
   * 
   * @param {string} email - User email
   * @returns {Promise<Object|null>} User object or null if not found
   */
  async findByEmail(email) {
    try {
      // In a real implementation, this would query the database
      return this.users.find(user => user.email === email) || null;
    } catch (error) {
      throw new Error(`Database error: ${error.message}`);
    }
  }

  /**
   * Saves a new user
   * 
   * @param {Object} userData - User data to save
   * @returns {Promise<Object>} Saved user object with generated ID
   */
  async save(userData) {
    try {
      // Generate a UUID-like ID
      const id = this.generateId();
      
      // Create timestamps
      const now = new Date().toISOString();
      
      // Create user object
      const user = {
        ...userData,
        id,
        createdAt: now,
        updatedAt: now
      };
      
      // In a real implementation, this would insert into the database
      this.users.push(user);
      
      return user;
    } catch (error) {
      throw new Error(`Database error: ${error.message}`);
    }
  }

  /**
   * Updates an existing user
   * 
   * @param {string} id - User ID
   * @param {Object} userData - User data to update
   * @returns {Promise<Object>} Updated user object
   * @throws {Error} If user not found
   */
  async update(id, userData) {
    try {
      // Find user index
      const index = this.users.findIndex(user => user.id === id);
      
      if (index === -1) {
        throw new Error('User not found');
      }
      
      // Update user
      const updatedUser = {
        ...this.users[index],
        ...userData,
        updatedAt: new Date().toISOString()
      };
      
      // In a real implementation, this would update the database
      this.users[index] = updatedUser;
      
      return updatedUser;
    } catch (error) {
      throw new Error(`Database error: ${error.message}`);
    }
  }

  /**
   * Deletes a user
   * 
   * @param {string} id - User ID
   * @returns {Promise<boolean>} True if user was deleted
   * @throws {Error} If user not found
   */
  async delete(id) {
    try {
      // Find user index
      const index = this.users.findIndex(user => user.id === id);
      
      if (index === -1) {
        throw new Error('User not found');
      }
      
      // In a real implementation, this would delete from the database
      this.users.splice(index, 1);
      
      return true;
    } catch (error) {
      throw new Error(`Database error: ${error.message}`);
    }
  }

  /**
   * Generates a UUID-like ID
   * 
   * @returns {string} Generated ID
   */
  generateId() {
    // Simple UUID-like implementation
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

module.exports = { UserRepository }; 