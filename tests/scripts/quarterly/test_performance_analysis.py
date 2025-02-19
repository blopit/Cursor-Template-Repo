"""Tests for the quarterly performance analysis script."""
import json
from unittest.mock import Mock, patch
import pytest
from pathlib import Path
from scripts.quarterly.performance_analysis import (
    check_response_times,
    check_resource_usage,
    check_error_rates,
    check_performance_patterns,
    analyze_performance_trends,
    generate_report
)

@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def sample_response_data():
    return {
        "endpoints": [
            {
                "path": "/api/users",
                "method": "GET",
                "avg_response_time": 150,
                "p95_response_time": 250,
                "p99_response_time": 350
            }
        ]
    }

@pytest.fixture
def sample_resource_data():
    return {
        "cpu_usage": [
            {
                "timestamp": "2024-02-19T12:00:00Z",
                "usage_percent": 45.5
            }
        ],
        "memory_usage": [
            {
                "timestamp": "2024-02-19T12:00:00Z",
                "usage_mb": 1024.5
            }
        ],
        "disk_usage": [
            {
                "timestamp": "2024-02-19T12:00:00Z",
                "usage_percent": 75.5
            }
        ]
    }

def test_check_response_times(mock_subprocess):
    # Arrange
    response_output = json.dumps({
        "endpoints": [
            {
                "path": "/api/users",
                "method": "GET",
                "avg_response_time": 150
            }
        ]
    })
    mock_subprocess.return_value.stdout = response_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_response_times()

    # Assert
    assert "endpoints" in result
    assert len(result["endpoints"]) == 1
    assert result["endpoints"][0]["path"] == "/api/users"
    mock_subprocess.assert_called_once()

def test_check_resource_usage(mock_subprocess):
    # Arrange
    resource_output = json.dumps({
        "cpu_usage": [{"usage_percent": 45.5}],
        "memory_usage": [{"usage_mb": 1024.5}],
        "disk_usage": [{"usage_percent": 75.5}]
    })
    mock_subprocess.return_value.stdout = resource_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_resource_usage()

    # Assert
    assert "cpu_usage" in result
    assert "memory_usage" in result
    assert "disk_usage" in result
    assert result["cpu_usage"][0]["usage_percent"] == 45.5
    mock_subprocess.assert_called_once()

def test_check_error_rates(mock_subprocess):
    # Arrange
    error_output = json.dumps({
        "error_rates": [
            {
                "endpoint": "/api/users",
                "error_count": 50,
                "total_requests": 1000,
                "error_rate": 0.05
            }
        ]
    })
    mock_subprocess.return_value.stdout = error_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_error_rates()

    # Assert
    assert "error_rates" in result
    assert len(result["error_rates"]) == 1
    assert result["error_rates"][0]["endpoint"] == "/api/users"
    mock_subprocess.assert_called_once()

def test_check_performance_patterns(mock_subprocess):
    # Arrange
    patterns_output = json.dumps({
        "patterns": [
            {
                "type": "Response Time Spike",
                "frequency": "Daily",
                "avg_impact": 250,
                "affected_endpoints": ["/api/users"]
            }
        ]
    })
    mock_subprocess.return_value.stdout = patterns_output
    mock_subprocess.return_value.returncode = 0

    # Act
    result = check_performance_patterns()

    # Assert
    assert "patterns" in result
    assert len(result["patterns"]) == 1
    assert result["patterns"][0]["type"] == "Response Time Spike"
    mock_subprocess.assert_called_once()

def test_analyze_performance_trends(sample_response_data, sample_resource_data):
    # Arrange
    performance_data = {
        "response_times": sample_response_data["endpoints"],
        "resource_usage": {
            "cpu": sample_resource_data["cpu_usage"],
            "memory": sample_resource_data["memory_usage"],
            "disk": sample_resource_data["disk_usage"]
        }
    }
    
    # Act
    analysis = analyze_performance_trends(performance_data)
    
    # Assert
    assert "Response Time Analysis" in analysis
    assert "/api/users" in analysis
    assert "Resource Usage Analysis" in analysis
    assert "CPU Usage" in analysis

def test_generate_report(tmp_path):
    # Arrange
    response_data = {
        "endpoints": [
            {
                "path": "/api/users",
                "method": "GET",
                "avg_response_time": 150
            }
        ]
    }
    resource_data = {
        "cpu_usage": [{"usage_percent": 45.5}],
        "memory_usage": [{"usage_mb": 1024.5}],
        "disk_usage": [{"usage_percent": 75.5}]
    }
    error_data = {
        "error_rates": [
            {
                "endpoint": "/api/users",
                "error_rate": 0.05
            }
        ]
    }
    patterns_data = {
        "patterns": [
            {
                "type": "Response Time Spike",
                "frequency": "Daily"
            }
        ]
    }
    
    log_dir = tmp_path / ".cursor" / "logs" / "performance_analysis"
    log_dir.mkdir(parents=True)
    
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        # Act
        report_path = generate_report(
            response_data,
            resource_data,
            error_data,
            patterns_data
        )
        
        # Assert
        mock_mkdir.assert_called_with(parents=True, exist_ok=True)
        assert isinstance(report_path, Path)

@pytest.mark.integration
def test_full_performance_analysis_workflow(tmp_path):
    """Integration test for the full performance analysis workflow."""
    # Arrange
    log_dir = tmp_path / ".cursor" / "logs" / "performance_analysis"
    log_dir.mkdir(parents=True)
    
    with patch('scripts.quarterly.performance_analysis.check_response_times') as mock_response, \
         patch('scripts.quarterly.performance_analysis.check_resource_usage') as mock_resource, \
         patch('scripts.quarterly.performance_analysis.check_error_rates') as mock_error, \
         patch('scripts.quarterly.performance_analysis.check_performance_patterns') as mock_patterns, \
         patch('scripts.quarterly.performance_analysis.generate_report') as mock_report:
        
        # Setup mock returns
        mock_response.return_value = {"endpoints": []}
        mock_resource.return_value = {"cpu_usage": [], "memory_usage": [], "disk_usage": []}
        mock_error.return_value = {"error_rates": []}
        mock_patterns.return_value = {"patterns": []}
        
        from scripts.quarterly.performance_analysis import main
        
        # Act
        main()
        
        # Assert
        mock_response.assert_called_once()
        mock_resource.assert_called_once()
        mock_error.assert_called_once()
        mock_patterns.assert_called_once()
        mock_report.assert_called_once()

def test_error_handling_response_check(mock_subprocess):
    # Arrange
    mock_subprocess.side_effect = FileNotFoundError("ab-bench not found")

    # Act
    result = check_response_times()

    # Assert
    assert result == {} 