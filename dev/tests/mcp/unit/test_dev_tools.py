import os
import sys
import pytest
from pathlib import Path

def test_dev_tools_structure():
    """Test that development tools are properly organized."""
    # Test that dev directory exists
    dev_dir = Path('dev')
    assert dev_dir.exists()
    assert dev_dir.is_dir()
    
    # Test that tools directory exists
    tools_dir = dev_dir / 'tools'
    assert tools_dir.exists()
    assert tools_dir.is_dir()
    
    # Test that scripts directory exists
    scripts_dir = dev_dir / 'scripts'
    assert scripts_dir.exists()
    assert scripts_dir.is_dir()

def test_dev_tools_imports():
    """Test that development tools can be imported."""
    # Add dev directory to Python path
    dev_tools_path = os.path.abspath('dev/tools')
    if dev_tools_path not in sys.path:
        sys.path.append(dev_tools_path)
    
    try:
        # Test importing tools
        import llm_api
        import web_scraper
        import search_engine
        import screenshot_utils
        
        # Test basic attributes
        assert hasattr(llm_api, 'query_llm')
        assert hasattr(web_scraper, 'scrape_urls')
        assert hasattr(search_engine, 'search')
        assert hasattr(screenshot_utils, 'take_screenshot_sync')
    except ImportError as e:
        pytest.fail(f"Failed to import development tools: {e}")

def test_dev_requirements():
    """Test that development requirements are installed."""
    import pkg_resources
    
    with open('requirements-dev.txt') as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith('#') and not line.startswith('-r')
        ]
    
    for requirement in requirements:
        try:
            pkg_resources.require(requirement)
        except pkg_resources.DistributionNotFound:
            pytest.fail(f"Required package not found: {requirement}")
        except pkg_resources.VersionConflict:
            pytest.fail(f"Version conflict for package: {requirement}") 