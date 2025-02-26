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
    env_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
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

def test_llm_api_keys_exist(dev_environment):
    """Test that LLM API keys are set."""
    # Test OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    assert openai_key is not None, "OpenAI API key not found"
    
    # Test Anthropic API key
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    assert anthropic_key is not None, "Anthropic API key not found"
    
    # Test Google API key
    google_key = os.getenv('GOOGLE_API_KEY')
    assert google_key is not None, "Google API key not found"

@pytest.mark.asyncio
async def test_llm_imports(dev_environment):
    """Test that LLM libraries are properly installed."""
    # Test OpenAI
    import openai
    assert openai.__version__ >= '1.63.2'
    
    # Test Anthropic
    import anthropic
    assert anthropic.__version__ >= '0.46.0'
    
    # Test Google Generative AI
    import google.generativeai as genai
    assert genai.__package__ == 'google.generativeai' 