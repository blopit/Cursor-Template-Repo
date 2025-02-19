"""Tests for the daily dependency check script."""
import json
from unittest.mock import Mock, patch
import pytest
from pathlib import Path
from scripts.daily.check_dependencies import (
    check_outdated_packages,
    check_dependency_conflicts,
    check_unused_dependencies,
    check_package_licenses,
    analyze_dependency_trends,
    generate_report
)

@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_log_dir(tmp_path):
    """Create a mock log directory for testing."""
    log_dir = tmp_path / ".cursor" / "logs" / "dependency_checks"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

@pytest.fixture
def sample_outdated_data():
    return {
        "outdated": [
            {
                "name": "requests",
                "current_version": "2.25.1",
                "latest_version": "2.31.0",
                "type": "minor"
            }
        ]
    }

@pytest.fixture
def sample_conflicts_data():
    return {
        "conflicts": [
            {
                "package": "tensorflow",
                "current_version": "2.5.0",
                "conflicting_deps": [
                    {
                        "package": "numpy",
                        "required_version": ">=1.19.2,<1.20",
                        "installed_version": "1.21.0"
                    }
                ]
            }
        ]
    }

def test_check_outdated_packages(mock_subprocess):
    # Arrange
    outdated_output = json.dumps({
        "outdated": [
            {
                "name": "requests",
                "current_version": "2.25.1",
                "latest_version": "2.31.0"
            }
        ]
    })
    mock_subprocess.return_value.stdout = outdated_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_outdated_packages()

    # Assert
    assert "outdated" in result
    assert len(result["outdated"]) == 1
    assert result["outdated"][0]["name"] == "requests"
    mock_subprocess.assert_called_once()

def test_check_dependency_conflicts():
    """Test dependency conflict checking."""
    result = check_dependency_conflicts()
    assert isinstance(result, dict)
    assert "conflicts" in result
    assert isinstance(result["conflicts"], list)

def test_check_unused_dependencies():
    """Test unused dependency checking."""
    result = check_unused_dependencies()
    assert isinstance(result, dict)
    assert "unused" in result
    assert isinstance(result["unused"], list)

def test_check_package_licenses():
    """Test package license checking."""
    result = check_package_licenses()
    assert isinstance(result, dict)
    assert "licenses" in result
    assert isinstance(result["licenses"], list)

def test_analyze_dependency_trends(sample_outdated_data, sample_conflicts_data):
    # Arrange
    dependency_data = {
        "outdated": sample_outdated_data["outdated"],
        "conflicts": sample_conflicts_data["conflicts"]
    }
    
    # Act
    analysis = analyze_dependency_trends(dependency_data)
    
    # Assert
    assert "Outdated Packages" in analysis
    assert "requests" in analysis
    assert "Dependency Conflicts" in analysis
    assert "tensorflow" in analysis

def test_generate_report(mock_log_dir):
    """Test report generation."""
    conflicts_data = {
        "conflicts": [
            {
                "package": "requests",
                "version": "2.25.1",
                "conflict_with": "urllib3",
                "required_version": ">=2.0.0",
                "current_version": "1.26.6"
            }
        ]
    }
    
    unused_data = {
        "unused": [
            {
                "package": "pytest-mock",
                "version": "3.10.0",
                "last_used": "2024-01-01"
            }
        ]
    }
    
    licenses_data = {
        "licenses": [
            {
                "package": "requests",
                "version": "2.25.1",
                "license": "Apache-2.0",
                "compliant": True
            }
        ]
    }
    
    report_path = generate_report(conflicts_data, unused_data, licenses_data, log_dir=mock_log_dir)
    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.parent == mock_log_dir
    
    content = report_path.read_text()
    assert "Dependency Check Report" in content
    assert "Dependency Conflicts" in content
    assert "Unused Dependencies" in content
    assert "Package Licenses" in content
    assert "requests 2.25.1" in content
    assert "urllib3" in content
    assert "pytest-mock 3.10.0" in content
    assert "Apache-2.0" in content

@pytest.mark.integration
def test_full_dependency_check_workflow(tmp_path):
    """Integration test for the full dependency check workflow."""
    # Arrange
    log_dir = tmp_path / ".cursor" / "logs" / "dependency_checks"
    log_dir.mkdir(parents=True)
    
    with patch('scripts.daily.check_dependencies.check_outdated_packages') as mock_outdated, \
         patch('scripts.daily.check_dependencies.check_dependency_conflicts') as mock_conflicts, \
         patch('scripts.daily.check_dependencies.check_unused_dependencies') as mock_unused, \
         patch('scripts.daily.check_dependencies.check_package_licenses') as mock_licenses, \
         patch('scripts.daily.check_dependencies.generate_report') as mock_report:
        
        # Setup mock returns
        mock_outdated.return_value = {"outdated": []}
        mock_conflicts.return_value = {"conflicts": []}
        mock_unused.return_value = {"unused": []}
        mock_licenses.return_value = {"licenses": []}
        
        from scripts.daily.check_dependencies import main
        
        # Act
        main()
        
        # Assert
        mock_outdated.assert_called_once()
        mock_conflicts.assert_called_once()
        mock_unused.assert_called_once()
        mock_licenses.assert_called_once()
        mock_report.assert_called_once()

def test_error_handling_outdated_check(mock_subprocess):
    # Arrange
    mock_subprocess.side_effect = FileNotFoundError("pip not found")

    # Act
    result = check_outdated_packages()

    # Assert
    assert result == {}