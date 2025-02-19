import pytest
from pathlib import Path
from scripts.quarterly.code_quality_check import (
    check_code_complexity,
    check_code_style,
    generate_report
)

@pytest.fixture
def mock_log_dir(tmp_path):
    """Create a mock log directory for testing."""
    log_dir = tmp_path / ".cursor" / "logs" / "code_quality"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def test_check_code_complexity():
    """Test code complexity analysis."""
    result = check_code_complexity()
    assert isinstance(result, dict)
    assert "issues" in result
    assert isinstance(result["issues"], list)

def test_check_code_style():
    """Test code style analysis."""
    result = check_code_style()
    assert isinstance(result, dict)
    assert "issues" in result
    assert isinstance(result["issues"], list)

def test_generate_report(mock_log_dir):
    """Test report generation."""
    complexity_data = {"issues": [
        {
            "file": "test.py",
            "line": 10,
            "type": "high_complexity",
            "message": "Function has too many nested levels"
        }
    ]}
    
    style_data = {"issues": [
        {
            "file": "test.py",
            "line": 5,
            "type": "style_error",
            "message": "Missing whitespace around operator"
        }
    ]}
    
    report_path = generate_report(complexity_data, style_data, log_dir=mock_log_dir)
    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.parent == mock_log_dir
    
    content = report_path.read_text()
    assert "Code Quality Report" in content
    assert "Code Complexity Issues" in content
    assert "Code Style Issues" in content
    assert "Function has too many nested levels" in content
    assert "Missing whitespace around operator" in content 