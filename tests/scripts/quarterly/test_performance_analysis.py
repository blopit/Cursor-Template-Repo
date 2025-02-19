"""Tests for the quarterly performance analysis script."""
import json
from unittest.mock import Mock, patch
import pytest
from pathlib import Path
from scripts.quarterly.performance_analysis import (
    analyze_response_times,
    analyze_memory_usage,
    analyze_cpu_usage,
    analyze_error_rates,
    generate_report
)

@pytest.fixture
def mock_log_dir(tmp_path):
    """Create a mock log directory for testing."""
    log_dir = tmp_path / ".cursor" / "logs" / "performance"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

@pytest.fixture
def sample_response_data():
    return {
        "endpoints": [
            {
                "path": "/api/v1/users",
                "method": "GET",
                "avg_response_time": 150,
                "p95_response_time": 250,
                "p99_response_time": 350
            }
        ]
    }

@pytest.fixture
def sample_memory_data():
    return {
        "processes": [
            {
                "name": "web_server",
                "avg_memory_mb": 512,
                "peak_memory_mb": 1024
            }
        ]
    }

def test_analyze_response_times():
    """Test response time analysis."""
    result = analyze_response_times()
    assert isinstance(result, dict)
    assert "avg_response_time" in result
    assert "max_response_time" in result
    assert "min_response_time" in result
    assert "total_requests" in result

def test_analyze_memory_usage():
    """Test memory usage analysis."""
    result = analyze_memory_usage()
    assert isinstance(result, dict)
    assert "avg_memory_usage" in result
    assert "peak_memory_usage" in result
    assert "min_memory_usage" in result
    assert "samples_count" in result

def test_analyze_cpu_usage(sample_response_data):
    # Act
    result = analyze_cpu_usage(sample_response_data)
    
    # Assert
    assert isinstance(result, dict)
    assert "analysis" in result
    assert len(result["analysis"]) > 0
    assert "process" in result["analysis"][0]
    assert "avg_cpu_percent" in result["analysis"][0]

def test_analyze_error_rates(sample_response_data):
    # Act
    result = analyze_error_rates(sample_response_data)
    
    # Assert
    assert isinstance(result, dict)
    assert "analysis" in result
    assert len(result["analysis"]) > 0
    assert "error_type" in result["analysis"][0]
    assert "count" in result["analysis"][0]
    assert "trend" in result["analysis"][0]

def test_generate_report(mock_log_dir):
    """Test report generation."""
    response_times_data = {
        "avg_response_time": 150.0,
        "max_response_time": 200,
        "min_response_time": 100,
        "total_requests": 3
    }
    
    memory_usage_data = {
        "avg_memory_usage": 512.0,
        "peak_memory_usage": 600,
        "min_memory_usage": 450,
        "samples_count": 3
    }
    
    report_path = generate_report(response_times_data, memory_usage_data, log_dir=mock_log_dir)
    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.parent == mock_log_dir
    
    content = report_path.read_text()
    assert "Performance Analysis Report" in content
    assert "Response Times Analysis" in content
    assert "Memory Usage Analysis" in content
    assert "Average Response Time: 150.00ms" in content
    assert "Peak Memory Usage: 600MB" in content 