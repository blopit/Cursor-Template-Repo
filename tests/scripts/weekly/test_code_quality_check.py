"""Tests for the weekly code quality check script."""
import json
from unittest.mock import Mock, patch
import pytest
from scripts.weekly.code_quality_check import (
    check_code_complexity,
    check_code_duplication,
    check_test_coverage,
    check_documentation_coverage,
    check_style_compliance,
    analyze_complexity_trends,
    generate_report
)

@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def sample_complexity_data():
    return {
        "complexity": {
            "path/to/file.py": [
                {
                    "name": "complex_function",
                    "complexity": 15,
                    "line_number": 10
                }
            ]
        },
        "maintainability": {
            "path/to/file.py": 60.5
        }
    }

def test_check_code_complexity(mock_subprocess):
    # Arrange
    complexity_json = {
        "path/to/file.py": [
            {"name": "complex_function", "complexity": 15}
        ]
    }
    maintainability_json = {
        "path/to/file.py": 75.5
    }
    
    mock_subprocess.side_effect = [
        Mock(stdout=json.dumps(complexity_json), returncode=0),
        Mock(stdout=json.dumps(maintainability_json), returncode=0)
    ]

    # Act
    result = check_code_complexity()

    # Assert
    assert "complexity" in result
    assert "maintainability" in result
    assert mock_subprocess.call_count == 2

def test_check_code_duplication(mock_subprocess):
    # Arrange
    duplication_output = "Similar lines in 2 files\nfile1.py:10\nfile2.py:15"
    mock_subprocess.return_value.stdout = duplication_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_code_duplication()

    # Assert
    assert "Similar lines" in result
    assert "file1.py" in result
    mock_subprocess.assert_called_once()

def test_check_test_coverage(mock_subprocess, tmp_path):
    # Arrange
    coverage_data = {
        "totals": {
            "percent_covered": 85.5
        },
        "files": {
            "file1.py": {"summary": {"percent_covered": 90.0}},
            "file2.py": {"summary": {"percent_covered": 75.5}}
        }
    }
    
    coverage_file = tmp_path / "coverage.json"
    coverage_file.write_text(json.dumps(coverage_data))
    
    with patch('os.path.exists') as mock_exists, \
         patch('builtins.open', create=True) as mock_open:
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(coverage_data)
        
        # Act
        result = check_test_coverage()
        
        # Assert
        assert result["totals"]["percent_covered"] == 85.5
        assert len(result["files"]) == 2

def test_check_documentation_coverage(mock_subprocess):
    # Arrange
    doc_output = "Undocumented: 25.5%\nDocumented: 74.5%"
    mock_subprocess.return_value.stdout = doc_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_documentation_coverage()

    # Assert
    assert "Documented: 74.5%" in result
    mock_subprocess.assert_called_once()

def test_check_style_compliance(mock_subprocess):
    # Arrange
    style_output = "file1.py:10:1: E101 indentation contains mixed spaces and tabs"
    mock_subprocess.return_value.stdout = style_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_style_compliance()

    # Assert
    assert "E101" in result
    assert "indentation" in result
    mock_subprocess.assert_called_once()

def test_analyze_complexity_trends(sample_complexity_data):
    # Act
    analysis = analyze_complexity_trends(sample_complexity_data)

    # Assert
    assert "High Complexity Functions:" in analysis
    assert "path/to/file.py::complex_function" in analysis
    assert "complexity: 15" in analysis
    assert "Low Maintainability Files:" in analysis
    assert "MI: 60.5" in analysis

def test_generate_report(tmp_path):
    # Arrange
    complexity_data = {
        "complexity": {
            "file.py": [{"name": "func", "complexity": 12}]
        },
        "maintainability": {"file.py": 70.0}
    }
    duplication = "Similar lines found"
    coverage = {
        "totals": {"percent_covered": 85.5},
        "files": {
            "file.py": {"summary": {"percent_covered": 85.5}}
        }
    }
    documentation = "Documentation coverage: 75%"
    style = "Style issues found"
    
    log_dir = tmp_path / ".cursor" / "logs" / "code_quality"
    log_dir.mkdir(parents=True)
    
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        # Act
        generate_report(
            complexity_data,
            duplication,
            coverage,
            documentation,
            style
        )
        
        # Assert
        mock_mkdir.assert_called_with(parents=True, exist_ok=True)

@pytest.mark.integration
def test_full_code_quality_workflow(tmp_path):
    """Integration test for the full code quality check workflow."""
    # Arrange
    log_dir = tmp_path / ".cursor" / "logs" / "code_quality"
    log_dir.mkdir(parents=True)
    
    with patch('scripts.weekly.code_quality_check.check_code_complexity') as mock_complexity, \
         patch('scripts.weekly.code_quality_check.check_code_duplication') as mock_duplication, \
         patch('scripts.weekly.code_quality_check.check_test_coverage') as mock_coverage, \
         patch('scripts.weekly.code_quality_check.check_documentation_coverage') as mock_documentation, \
         patch('scripts.weekly.code_quality_check.check_style_compliance') as mock_style, \
         patch('scripts.weekly.code_quality_check.generate_report') as mock_report:
        
        # Setup mock returns
        mock_complexity.return_value = {"complexity": {}, "maintainability": {}}
        mock_duplication.return_value = "No duplication found"
        mock_coverage.return_value = {"totals": {"percent_covered": 85.5}}
        mock_documentation.return_value = "Documentation: 75%"
        mock_style.return_value = "No style issues"
        
        from scripts.weekly.code_quality_check import main
        
        # Act
        main()
        
        # Assert
        mock_complexity.assert_called_once()
        mock_duplication.assert_called_once()
        mock_coverage.assert_called_once()
        mock_documentation.assert_called_once()
        mock_style.assert_called_once()
        mock_report.assert_called_once()

def test_error_handling_complexity_check(mock_subprocess):
    # Arrange
    mock_subprocess.side_effect = FileNotFoundError("radon not found")

    # Act
    result = check_code_complexity()

    # Assert
    assert result == {} 