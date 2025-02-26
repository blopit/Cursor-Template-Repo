# Authentication Service (TDD Implementation)

This project demonstrates the implementation of an authentication service following the Test-Driven Development (TDD) approach within a Waterfall-TDD hybrid model. It provides functionality for user registration, login, password management, and profile updates.

## Project Structure

```
├── docs/
│   ├── requirements/       # Requirements documentation
│   │   └── REQ-AUTH-001.md # User authentication requirements
│   └── design/             # Design documentation
│       └── DES-AUTH-001.md # User authentication design
├── src/
│   ├── services/           # Business services
│   │   ├── auth-service.js     # Authentication service
│   │   ├── email-service.js    # Email service
│   │   └── password-service.js # Password service
│   ├── repositories/       # Data access layer
│   │   └── user-repository.js  # User repository
│   └── index.js            # Main application entry point
└── tests/
    └── auth/               # Authentication tests
        └── registration.test.js # User registration tests
```

## Features

- **User Registration**: Register new users with email, password, and profile information
- **Input Validation**: Validate email format, password complexity, and required fields
- **Email Verification**: Send verification emails to new users
- **Password Security**: Securely hash and verify passwords
- **Error Handling**: Comprehensive error handling for various scenarios

## Development Approach

This project follows the Waterfall-TDD hybrid model, which combines the structured phase-based approach of Waterfall with the quality-focused iterative practices of TDD:

1. **Requirements Analysis**: Documented in `docs/requirements/REQ-AUTH-001.md`
2. **System Design**: Documented in `docs/design/DES-AUTH-001.md`
3. **Implementation (TDD)**:
   - Write failing tests first (`tests/auth/registration.test.js`)
   - Implement minimal code to pass tests (`src/services/auth-service.js`)
   - Refactor while maintaining passing tests
4. **Verification & Quality Gates**: All tests must pass before proceeding
5. **Deployment & Maintenance**: Automated deployment through CI/CD pipeline

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/auth-service-tdd.git
cd auth-service-tdd

# Install dependencies
npm install
```

### Running the Application

```bash
# Start the application
npm start
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests with coverage report
npm run test:coverage

# Run tests in watch mode (for development)
npm run test:watch
```

## Code Quality Standards

- **Test Coverage**: Minimum 80% code coverage required
- **Documentation**: All classes, methods, and functions are documented
- **Error Handling**: Comprehensive error handling for all operations
- **Security**: Password hashing, input validation, and secure defaults

## Future Enhancements

- Implement login functionality
- Add password reset functionality
- Implement profile management
- Add session management
- Integrate with a real database
- Implement proper email sending

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Purpose

This template helps you:
- Set up a well-organized project structure for AI-assisted development
- Implement best practices for code quality and maintenance
- Automate common development tasks
- Maintain consistent coding standards
- Track and optimize AI token usage

## 📁 Project Structure

```
.
├── .cursor/                    # Cursor-specific configurations
│   ├── rules/                 # Development rules and guidelines
│   ├── metrics/              # AI usage metrics
│   └── logs/                 # Operation logs
├── scripts/                   # Maintenance and utility scripts
│   ├── daily/               # Daily maintenance tasks
│   ├── weekly/             # Weekly code quality checks
│   ├── monthly/            # Monthly security audits
│   └── quarterly/          # Quarterly performance analysis
├── tests/                    # Test files
├── tools/                    # Development tools and utilities
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

1. **Use this template**
   ```bash
   git clone https://github.com/yourusername/Cursor-Template.git your-project
   cd your-project
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

## 🛠️ Maintenance Scripts

### Daily Checks
- `scripts/daily/check_dependencies.py`: Monitors package dependencies
  ```bash
  ./scripts/daily/check_dependencies.py
  ```

### Weekly Checks
- `scripts/weekly/code_quality_check.py`: Analyzes code quality
  ```bash
  ./scripts/weekly/code_quality_check.py
  ```

### Monthly Checks
- `scripts/monthly/security_audit.py`: Performs security audits
  ```bash
  ./scripts/monthly/security_audit.py
  ```

### Quarterly Checks
- `scripts/quarterly/performance_analysis.py`: Analyzes system performance
  ```bash
  ./scripts/quarterly/performance_analysis.py
  ```

## 📋 Development Guidelines

### Test-Driven Development
This template follows TDD practices:
1. Write tests first
2. Implement minimal code to pass tests
3. Refactor while maintaining test coverage

### Code Quality Standards
- Maintain test coverage above 80%
- Follow PEP 8 style guidelines
- Document all public APIs
- Use type hints

### AI-Assisted Development
- Utilize Cursor's AI capabilities for:
  - Code generation
  - Refactoring
  - Documentation
  - Testing
- Track token usage and costs
- Follow AI-specific best practices

## 🔍 Quality Gates

- All tests must pass
- Code coverage >= 80%
- No security vulnerabilities
- All dependencies up to date
- Documentation complete

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes
   ```bash
   git commit -m "[Cursor] Add amazing feature"
   ```
4. Push to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Cursor](https://cursor.sh/) - The AI-first IDE
- OpenAI - For GPT models
- Anthropic - For Claude models
- Contributors to the maintenance scripts and tools

## 🔗 Useful Links

- [Cursor Documentation](https://cursor.sh/docs)
- [Python Best Practices](https://docs.python-guide.org/)
- [Test-Driven Development Guide](https://www.agilealliance.org/glossary/tdd/)

# Cursor Rules Structure

## Recommended Structure
```
.cursor/
├── rules/
│   ├── core/                 # Fundamental system rules
│   ├── tech/                 # Technology-specific rules
│   │   ├── typescript/       # TypeScript specific rules
│   │   ├── python/           # Python specific rules
│   │   └── ...
│   ├── workflows/            # Workflow and process rules
│   ├── patterns/             # Common code patterns and solutions
│   └── project/              # Project-specific rules
└── ...
```

## Implementation Steps
1. Move rules from `awesome-cursor-rules-mdc` to appropriate directories
2. Ensure proper glob patterns in each MDC file
3. Update rule references in `.cursorrules`

## About Cursor Rules

Cursor rules are instructions for the AI to follow when working with your codebase. They help ensure consistency, quality, and efficiency in development.

### Benefits of Structured Rules
- **Consistency**: Everyone follows the same practices
- **Quality**: Nothing important gets forgotten
- **Efficiency**: No need to repeat instructions for common tasks

### How Rules Work
- Rules are defined in `.mdc` files (Markdown Cursor)
- Each rule has a description and glob patterns to match files
- Rules can be organized by technology, workflow, or purpose
- The AI applies rules based on priority and specificity

### Using Rules
- Reference rules in your conversations with the AI
- The AI will automatically apply rules that match the files you're working with
- You can create custom rules for your specific project needs

## Getting Started
To use these rules effectively:
1. Familiarize yourself with the rule categories
2. Reference relevant rules when working with the AI
3. Create custom rules for your specific project needs 