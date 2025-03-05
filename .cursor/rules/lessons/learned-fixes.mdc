---
description: Common fixes and solutions from past experiences
globs: *.py,*.log,error_*.png,*_error.png
---
# Lessons Learned Rules

## Environment Setup
- Use Python venv in ./venv
- Include debug info in program output
- Read files before editing
- Handle file encodings properly
- Ensure database drivers (psycopg2) are installed
- Use environment variables for configuration
- Set proper Python path for imports

## Database Setup
- Start with minimal schema for prototypes
- Use SQLAlchemy for ORM
- Implement proper database migrations
- Handle database connections safely
- Use connection pooling
- Set up cascading deletes where appropriate
- Add proper foreign key constraints

## API Development
- Use FastAPI for rapid prototyping
- Implement proper Pydantic models
- Add proper type hints
- Handle async operations correctly
- Implement proper error handling
- Use dependency injection for database sessions
- Document API endpoints

## AI Integration
- Pin OpenAI package version or use latest API format
- Handle API versioning changes (openai>=1.0.0 vs <1.0.0)
- Implement proper error handling for AI responses
- Use system messages for context
- Structure function calls properly
- Keep conversation context for better assistance
- Validate AI responses before applying changes

## Best Practices
- Follow conventional commits
- Write clear documentation
- Test thoroughly
- Monitor performance
- Keep prototypes lean but extensible
- Use proper code organization
- Handle resource cleanup
- Check package compatibility before upgrading

## Common Fixes
- Use seaborn-v0_8 style name
- Handle UTF-8 encoding
- Add stderr debug info
- Clean stdout output
- Fix import paths in migration files
- Handle database connection errors
- Implement proper error responses
- Pin package versions for stability
- Update OpenAI API calls for v1.0.0

# Common Issues and Their Fixes

## Python Module Import Issues

### Issue: ModuleNotFoundError: No module named 'src'
**Symptoms:**
- Error when running uvicorn: `ModuleNotFoundError: No module named 'src'`
- Happens even when PYTHONPATH is set
- Usually occurs when starting the server

**Root Cause:**
- The Python interpreter can't find the `src` module because we're not running the command from the correct directory
- Simply setting PYTHONPATH isn't enough if we're not in the directory containing the `src` folder

**Solution:**
1. Always run the server from inside the backend directory
2. Use this command sequence:
```bash
cd backend  # Make sure you're in the backend directory
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Add current directory to Python path
uvicorn src.main:app --reload --port 8000  # Start the server
```

**Prevention:**
- Create a start script that ensures correct directory
- Add directory structure checks
- Document the correct working directory in README

## Best Practices for Issue Resolution
1. Document the exact error message
2. Note the context (what command was being run)
3. Identify the root cause
4. Provide a step-by-step solution
5. Add prevention measures
6. Update documentation

## Version Comparison Issues

### Issue: Incorrect Version Number Comparison
**Symptoms:**
- Version comparison fails for versions like "3.10" vs "3.9"
- Using `bc` or simple string comparison gives wrong results
- Error messages show version requirements not met when they actually are

**Root Cause:**
- Version numbers are not simple decimal numbers
- "3.10" is greater than "3.9", but string or decimal comparison might say otherwise
- Using `bc` for floating-point comparison doesn't handle version numbers correctly

**Solution:**
Instead of using `bc` or string comparison, use Python's built-in version comparison:
```bash
# Wrong way:
if (( $(echo "$VERSION < 3.9" | bc -l) )); then
    echo "Version too low"
fi

# Right way:
if ! python3 -c 'import sys; exit(0) if sys.version_info >= (3, 9) else exit(1)'; then
    echo "Version too low"
fi
```

**Prevention:**
- Always use proper version comparison tools
- For Python versions, use `sys.version_info`
- For other version comparisons, consider using `sort -V` or dedicated version comparison tools
- Add test cases with edge case versions (e.g., 3.9, 3.10, 3.11)

## Dependency Chain Issues

### Issue: Missing Nested Dependencies
**Symptoms:**
- Server starts but fails with `ModuleNotFoundError`
- Error occurs in imported modules rather than main file
- Dependencies are discovered only when running the application

**Example Error:**
```
ModuleNotFoundError: No module named 'elevenlabs'
Traceback shows:
main.py -> api/chat.py -> services/chat_service.py -> elevenlabs import fails
```

**Root Cause:**
- Dependency chain not fully documented
- Dependencies are imported in nested modules
- Requirements file may be incomplete
- Virtual environment might not have all packages

**Solution:**
1. Install the missing package:
```bash
pip install elevenlabs
```
2. Update requirements.txt:
```bash
pip freeze > requirements.txt
```

**Prevention:**
- Use tools like `pipreqs` to scan all imports
- Test with fresh virtual environment
- Document all third-party services
- Add dependency check to startup script
- Keep requirements.txt updated

## Python Version Compatibility Issues

### Issue: Package Requires Newer Python Features
**Symptoms:**
- `ImportError: cannot import name 'Literal' from 'typing'`
- Package installs but fails when importing
- Errors about missing typing features

**Example Error:**
```
ImportError: cannot import name 'Literal' from 'typing'
Traceback shows:
main.py -> chat.py -> chat_service.py -> elevenlabs -> typing.Literal missing
```

**Root Cause:**
- Package requires newer Python features (e.g., typing.Literal from Python 3.8+)
- Package installed successfully but runtime features missing
- pip doesn't always check Python version compatibility

**Solution:**
1. Check package's Python version requirements before installing
2. Use `typing_extensions` for backported features
3. Pin package versions that work with your Python version

**Prevention:**
- Add Python version check before package operations
- Use `python_requires` in setup.py
- Document minimum Python version
- Test in fresh environment
- Use version-specific requirements files

## Optional Feature Handling

### Issue: Non-Critical Feature Breaking Core Functionality
**Symptoms:**
- Application fails to start due to optional feature
- Import errors in non-essential modules
- Feature-specific dependencies causing system-wide issues

**Example Error:**
```python
ImportError: cannot import name 'Literal' from 'typing'
# When trying to import elevenlabs for optional voice features
```

**Root Cause:**
- Optional features not properly isolated
- Dependencies for non-critical features blocking core functionality
- Missing graceful degradation

**Solution:**
Use try-except pattern for optional features:
```python
# Wrong way:
from optional_feature import Feature  # Crashes if not available

# Right way:
try:
    from optional_feature import Feature
    FEATURE_ENABLED = True
except ImportError:
    FEATURE_ENABLED = False
    print("Feature disabled: dependency not available")

def use_feature():
    if not FEATURE_ENABLED:
        return None
    # Feature implementation
```

**Prevention:**
- Isolate optional features
- Use feature flags
- Implement graceful degradation
- Document optional dependencies
- Test both with and without optional features

<rule>
name: lessons_learned
description: Rules based on experience and fixes
filters:
  - type: event
    pattern: "error_fix|improvement"
  - type: content
    pattern: "fix|improve|learn"

actions:
  - type: enforce
    conditions:
      - pattern: "debug_info"
        message: "Include debug information"
      - pattern: "file_read"
        message: "Read file before editing"
      - pattern: "db_session"
        message: "Properly handle database sessions"
      - pattern: "error_handling"
        message: "Implement proper error handling"
      - pattern: "api_version"
        message: "Check API version compatibility"

  - type: suggest
    message: |
      Remember these lessons:
      1. Use virtual environment
      2. Include debug info
      3. Read before edit
      4. Document fixes
      5. Update rules
      6. Handle resources properly
      7. Keep prototypes simple
      8. Plan for extensibility
      9. Check API versions
      10. Pin package versions

metadata:
  priority: high
  version: 1.2
</rule> 
