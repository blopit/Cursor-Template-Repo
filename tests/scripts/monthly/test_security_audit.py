"""Tests for the monthly security audit script."""
import json
from unittest.mock import Mock, patch
import pytest
from pathlib import Path
from scripts.monthly.security_audit import (
    check_dependency_vulnerabilities,
    check_secrets_exposure,
    check_security_patterns,
    check_api_key_rotation,
    analyze_security_trends,
    generate_report
)

@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def sample_vulnerability_data():
    return {
        "vulnerabilities": [
            {
                "package": "requests",
                "version": "2.25.1",
                "severity": "HIGH",
                "description": "Potential SSRF vulnerability",
                "fix_version": "2.26.0"
            }
        ]
    }

@pytest.fixture
def sample_secrets_data():
    return {
        "exposed_secrets": [
            {
                "file": "config.py",
                "line": 10,
                "type": "API Key",
                "severity": "HIGH"
            }
        ]
    }

def test_check_dependency_vulnerabilities(mock_subprocess):
    # Arrange
    vuln_output = json.dumps({
        "vulnerabilities": [
            {
                "package": "requests",
                "version": "2.25.1",
                "severity": "HIGH"
            }
        ]
    })
    mock_subprocess.return_value.stdout = vuln_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_dependency_vulnerabilities()

    # Assert
    assert "vulnerabilities" in result
    assert len(result["vulnerabilities"]) == 1
    assert result["vulnerabilities"][0]["package"] == "requests"
    mock_subprocess.assert_called_once()

def test_check_secrets_exposure(mock_subprocess):
    # Arrange
    secrets_output = json.dumps({
        "exposed_secrets": [
            {
                "file": "config.py",
                "line": 10,
                "type": "API Key"
            }
        ]
    })
    mock_subprocess.return_value.stdout = secrets_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_secrets_exposure()

    # Assert
    assert "exposed_secrets" in result
    assert len(result["exposed_secrets"]) == 1
    assert result["exposed_secrets"][0]["file"] == "config.py"
    mock_subprocess.assert_called_once()

def test_check_security_patterns(mock_subprocess):
    # Arrange
    patterns_output = json.dumps({
        "issues": [
            {
                "file": "app.py",
                "line": 25,
                "pattern": "SQL Injection",
                "severity": "HIGH"
            }
        ]
    })
    mock_subprocess.return_value.stdout = patterns_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_security_patterns()

    # Assert
    assert "issues" in result
    assert len(result["issues"]) == 1
    assert result["issues"][0]["pattern"] == "SQL Injection"
    mock_subprocess.assert_called_once()

def test_check_api_key_rotation():
    # Arrange
    with patch('pathlib.Path.glob') as mock_glob, \
         patch('builtins.open', create=True) as mock_open:
        mock_glob.return_value = [Path('config.py')]
        mock_open.return_value.__enter__.return_value.read.return_value = """
        API_KEY = "abc123"  # Last rotated: 2024-01-01
        """
        
        # Act
        result = check_api_key_rotation()
        
        # Assert
        assert "api_keys" in result
        assert len(result["api_keys"]) > 0
        assert "config.py" in result["api_keys"][0]["file"]

def test_analyze_security_trends(sample_vulnerability_data, sample_secrets_data):
    # Arrange
    security_data = {
        "vulnerabilities": sample_vulnerability_data["vulnerabilities"],
        "secrets": sample_secrets_data["exposed_secrets"]
    }
    
    # Act
    analysis = analyze_security_trends(security_data)
    
    # Assert
    assert "High Severity Vulnerabilities" in analysis
    assert "requests" in analysis
    assert "Exposed Secrets" in analysis
    assert "config.py" in analysis

def test_generate_report(tmp_path):
    # Arrange
    vulnerability_data = {
        "vulnerabilities": [
            {
                "package": "requests",
                "version": "2.25.1",
                "severity": "HIGH"
            }
        ]
    }
    secrets_data = {
        "exposed_secrets": [
            {
                "file": "config.py",
                "line": 10,
                "type": "API Key"
            }
        ]
    }
    patterns_data = {
        "issues": [
            {
                "file": "app.py",
                "line": 25,
                "pattern": "SQL Injection"
            }
        ]
    }
    api_keys_data = {
        "api_keys": [
            {
                "file": "config.py",
                "last_rotation": "2024-01-01"
            }
        ]
    }
    
    log_dir = tmp_path / ".cursor" / "logs" / "security_audits"
    log_dir.mkdir(parents=True)
    
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        # Act
        report_path = generate_report(
            vulnerability_data,
            secrets_data,
            patterns_data,
            api_keys_data
        )
        
        # Assert
        mock_mkdir.assert_called_with(parents=True, exist_ok=True)
        assert isinstance(report_path, Path)

@pytest.mark.integration
def test_full_security_audit_workflow(tmp_path):
    """Integration test for the full security audit workflow."""
    # Arrange
    log_dir = tmp_path / ".cursor" / "logs" / "security_audits"
    log_dir.mkdir(parents=True)
    
    with patch('scripts.monthly.security_audit.check_dependency_vulnerabilities') as mock_vuln, \
         patch('scripts.monthly.security_audit.check_secrets_exposure') as mock_secrets, \
         patch('scripts.monthly.security_audit.check_security_patterns') as mock_patterns, \
         patch('scripts.monthly.security_audit.check_api_key_rotation') as mock_api_keys, \
         patch('scripts.monthly.security_audit.generate_report') as mock_report:
        
        # Setup mock returns
        mock_vuln.return_value = {"vulnerabilities": []}
        mock_secrets.return_value = {"exposed_secrets": []}
        mock_patterns.return_value = {"issues": []}
        mock_api_keys.return_value = {"api_keys": []}
        
        from scripts.monthly.security_audit import main
        
        # Act
        main()
        
        # Assert
        mock_vuln.assert_called_once()
        mock_secrets.assert_called_once()
        mock_patterns.assert_called_once()
        mock_api_keys.assert_called_once()
        mock_report.assert_called_once()

def test_error_handling_vulnerability_check(mock_subprocess):
    # Arrange
    mock_subprocess.side_effect = FileNotFoundError("safety not found")

    # Act
    result = check_dependency_vulnerabilities()

    # Assert
    assert result == {} 