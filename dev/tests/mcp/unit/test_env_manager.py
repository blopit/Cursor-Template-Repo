import os
import pytest
from pathlib import Path
from dev.tools.env_manager import backup_env, switch_environment, list_environments

@pytest.fixture
def temp_env_files(tmp_path):
    """Create temporary environment files for testing."""
    # Create test environment files
    (tmp_path / '.env.dev').write_text('DEV=true')
    (tmp_path / '.env.prod').write_text('PROD=true')
    (tmp_path / '.env').write_text('CURRENT=true')
    
    # Change to temp directory for tests
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    yield tmp_path
    
    # Cleanup and restore original directory
    os.chdir(original_dir)

def test_backup_env(temp_env_files):
    """Test environment file backup functionality."""
    env_path = temp_env_files / '.env'
    backup_path = backup_env(env_path)
    
    assert backup_path.exists()
    assert backup_path.name == '.env.backup'
    assert backup_path.read_text() == 'CURRENT=true'

def test_switch_environment(temp_env_files):
    """Test switching between environments."""
    # Switch to dev environment
    switch_environment('dev')
    
    env_path = temp_env_files / '.env'
    assert env_path.exists()
    if os.name != 'nt':  # Skip symlink check on Windows
        assert env_path.is_symlink()
        assert env_path.resolve() == temp_env_files / '.env.dev'

def test_switch_to_nonexistent_environment(temp_env_files):
    """Test switching to a non-existent environment."""
    with pytest.raises(FileNotFoundError):
        switch_environment('nonexistent')

def test_list_environments(temp_env_files, capsys):
    """Test listing available environments."""
    list_environments()
    captured = capsys.readouterr()
    
    assert 'dev' in captured.out
    assert 'prod' in captured.out 