import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from dev.tools.env_manager import switch_environment

@pytest.fixture(scope='module')
def dev_environment():
    """Set up development environment for tests."""
    # Store current environment
    original_env = {}
    env_vars = ['ENVIRONMENT', 'DEBUG', 'LOG_LEVEL', 'API_BASE_URL', 'FRONTEND_URL']
    for var in env_vars:
        original_env[var] = os.getenv(var)
    
    # Switch to dev environment
    switch_environment('dev')
    load_dotenv()
    
    yield
    
    # Restore original environment variables
    for var, value in original_env.items():
        if value is None:
            os.unsetenv(var)
        else:
            os.environ[var] = value

def test_environment_variables(dev_environment):
    """Test that required environment variables are set."""
    # Test environment type
    assert os.getenv('ENVIRONMENT') == 'development'
    
    # Test debug mode
    assert os.getenv('DEBUG') == 'true'
    
    # Test log level
    assert os.getenv('LOG_LEVEL') == 'DEBUG'

def test_python_environment(dev_environment):
    """Test Python environment setup."""
    # Test that we're running in a virtual environment
    assert os.getenv('VIRTUAL_ENV') is not None
    
    # Test that pytest is installed
    import pytest
    assert pytest.__version__ >= '8.3.4'

def test_api_configuration(dev_environment):
    """Test API configuration."""
    # Test API URLs are set
    assert os.getenv('API_BASE_URL') == 'http://localhost:8000'
    assert os.getenv('FRONTEND_URL') == 'http://localhost:3000' 