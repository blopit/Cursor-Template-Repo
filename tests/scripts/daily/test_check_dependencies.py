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

def test_check_dependency_conflicts(mock_subprocess):
    # Arrange
    conflicts_output = json.dumps({
        "conflicts": [
            {
                "package": "tensorflow",
                "conflicting_deps": ["numpy"]
            }
        ]
    })
    mock_subprocess.return_value.stdout = conflicts_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_dependency_conflicts()

    # Assert
    assert "conflicts" in result
    assert len(result["conflicts"]) == 1
    assert result["conflicts"][0]["package"] == "tensorflow"
    mock_subprocess.assert_called_once()

def test_check_unused_dependencies(mock_subprocess):
    # Arrange
    unused_output = json.dumps({
        "unused": [
            {
                "package": "unused-package",
                "size": "1.2MB"
            }
        ]
    })
    mock_subprocess.return_value.stdout = unused_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_unused_dependencies()

    # Assert
    assert "unused" in result
    assert len(result["unused"]) == 1
    assert result["unused"][0]["package"] == "unused-package"
    mock_subprocess.assert_called_once()

def test_check_package_licenses(mock_subprocess):
    # Arrange
    license_output = json.dumps({
        "licenses": [
            {
                "package": "requests",
                "license": "Apache-2.0",
                "approved": True
            }
        ]
    })
    mock_subprocess.return_value.stdout = license_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_package_licenses()

    # Assert
    assert "licenses" in result
    assert len(result["licenses"]) == 1
    assert result["licenses"][0]["package"] == "requests"
    mock_subprocess.assert_called_once()

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

def test_generate_report(tmp_path):
    # Arrange
    outdated_data = {
        "outdated": [
            {
                "name": "requests",
                "current_version": "2.25.1",
                "latest_version": "2.31.0"
            }
        ]
    }
    conflicts_data = {
        "conflicts": [
            {
                "package": "tensorflow",
                "conflicting_deps": ["numpy"]
            }
        ]
    }
    unused_data = {
        "unused": [
            {
                "package": "unused-package",
                "size": "1.2MB"
            }
        ]
    }
    license_data = {
        "licenses": [
            {
                "package": "requests",
                "license": "Apache-2.0"
            }
        ]
    }
    
    log_dir = tmp_path / ".cursor" / "logs" / "dependency_checks"
    log_dir.mkdir(parents=True)
    
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        # Act
        report_path = generate_report(
            outdated_data,
            conflicts_data,
            unused_data,
            license_data
        )
        
        # Assert
        mock_mkdir.assert_called_with(parents=True, exist_ok=True)
        assert isinstance(report_path, Path)

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