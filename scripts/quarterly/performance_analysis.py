#!/usr/bin/env python3
"""
Quarterly performance analysis script.
Analyzes:
1. API response times
2. Resource usage (CPU, Memory, Disk)
3. Error rates
4. Performance patterns
5. Long-term trends
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_response_times() -> Dict[str, List[Dict[str, Any]]]:
    """Check API endpoint response times using ab-bench."""
    try:
        result = subprocess.run(
            ['ab-bench', 'analyze', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking response times: {str(e)}")
        return {}

def check_resource_usage() -> Dict[str, List[Dict[str, Any]]]:
    """Check system resource usage trends."""
    try:
        result = subprocess.run(
            ['sys-metrics', 'collect', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking resource usage: {str(e)}")
        return {}

def check_error_rates() -> Dict[str, List[Dict[str, Any]]]:
    """Analyze API error rates from logs."""
    try:
        result = subprocess.run(
            ['log-analyzer', 'errors', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking error rates: {str(e)}")
        return {}

def check_performance_patterns() -> Dict[str, List[Dict[str, Any]]]:
    """Identify recurring performance patterns."""
    try:
        result = subprocess.run(
            ['perf-pattern', 'analyze', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking performance patterns: {str(e)}")
        return {}

def analyze_performance_trends(performance_data: Dict[str, Any]) -> str:
    """Analyze performance trends and provide recommendations."""
    analysis = []
    
    # Analyze response times
    if "response_times" in performance_data:
        analysis.append("Response Time Analysis:")
        for endpoint in performance_data["response_times"]:
            analysis.append(
                f"Endpoint: {endpoint['path']} ({endpoint['method']})\n"
                f"  Average: {endpoint.get('avg_response_time', 'N/A')}ms\n"
                f"  P95: {endpoint.get('p95_response_time', 'N/A')}ms\n"
                f"  P99: {endpoint.get('p99_response_time', 'N/A')}ms"
            )
    
    # Analyze resource usage
    if "resource_usage" in performance_data:
        analysis.append("\nResource Usage Analysis:")
        
        # CPU Analysis
        if "cpu" in performance_data["resource_usage"]:
            cpu_data = performance_data["resource_usage"]["cpu"]
            avg_cpu = sum(d["usage_percent"] for d in cpu_data) / len(cpu_data) if cpu_data else 0
            analysis.append(f"CPU Usage:\n  Average: {avg_cpu:.1f}%")
        
        # Memory Analysis
        if "memory" in performance_data["resource_usage"]:
            memory_data = performance_data["resource_usage"]["memory"]
            avg_memory = sum(d["usage_mb"] for d in memory_data) / len(memory_data) if memory_data else 0
            analysis.append(f"Memory Usage:\n  Average: {avg_memory:.1f}MB")
        
        # Disk Analysis
        if "disk" in performance_data["resource_usage"]:
            disk_data = performance_data["resource_usage"]["disk"]
            avg_disk = sum(d["usage_percent"] for d in disk_data) / len(disk_data) if disk_data else 0
            analysis.append(f"Disk Usage:\n  Average: {avg_disk:.1f}%")
    
    return "\n".join(analysis)

def generate_report(
    response_data: Dict[str, List[Dict[str, Any]]],
    resource_data: Dict[str, List[Dict[str, Any]]],
    error_data: Dict[str, List[Dict[str, Any]]],
    patterns_data: Dict[str, List[Dict[str, Any]]]
) -> Path:
    """Generate a comprehensive performance analysis report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path(".cursor") / "logs" / "performance_analysis"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = log_dir / f"performance_report_{timestamp}.txt"
    
    with open(report_path, 'w') as f:
        f.write("=== Performance Analysis Report ===\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Response Times
        f.write("=== API Response Times ===\n")
        if response_data.get("endpoints"):
            for endpoint in response_data["endpoints"]:
                f.write(
                    f"Endpoint: {endpoint['path']} ({endpoint['method']})\n"
                    f"Average Response Time: {endpoint['avg_response_time']}ms\n\n"
                )
        else:
            f.write("No response time data available.\n\n")
        
        # Resource Usage
        f.write("=== Resource Usage ===\n")
        if resource_data.get("cpu_usage"):
            f.write("CPU Usage:\n")
            for usage in resource_data["cpu_usage"]:
                f.write(f"  {usage['usage_percent']}%\n")
        
        if resource_data.get("memory_usage"):
            f.write("\nMemory Usage:\n")
            for usage in resource_data["memory_usage"]:
                f.write(f"  {usage['usage_mb']}MB\n")
        
        if resource_data.get("disk_usage"):
            f.write("\nDisk Usage:\n")
            for usage in resource_data["disk_usage"]:
                f.write(f"  {usage['usage_percent']}%\n")
        f.write("\n")
        
        # Error Rates
        f.write("=== Error Rates ===\n")
        if error_data.get("error_rates"):
            for error in error_data["error_rates"]:
                f.write(
                    f"Endpoint: {error['endpoint']}\n"
                    f"Error Rate: {error['error_rate']*100:.2f}%\n\n"
                )
        else:
            f.write("No error rate data available.\n\n")
        
        # Performance Patterns
        f.write("=== Performance Patterns ===\n")
        if patterns_data.get("patterns"):
            for pattern in patterns_data["patterns"]:
                f.write(
                    f"Pattern: {pattern['type']}\n"
                    f"Frequency: {pattern['frequency']}\n\n"
                )
        else:
            f.write("No performance patterns detected.\n\n")
        
        # Trend Analysis
        f.write("=== Trend Analysis ===\n")
        f.write(analyze_performance_trends({
            "response_times": response_data.get("endpoints", []),
            "resource_usage": {
                "cpu": resource_data.get("cpu_usage", []),
                "memory": resource_data.get("memory_usage", []),
                "disk": resource_data.get("disk_usage", [])
            }
        }))
    
    logger.info(f"Report generated: {report_path}")
    return report_path

def main():
    """Run quarterly performance analysis."""
    logger.info("Starting quarterly performance analysis...")
    
    response_data = check_response_times()
    logger.info("Completed response time analysis")
    
    resource_data = check_resource_usage()
    logger.info("Completed resource usage analysis")
    
    error_data = check_error_rates()
    logger.info("Completed error rate analysis")
    
    patterns_data = check_performance_patterns()
    logger.info("Completed performance pattern analysis")
    
    report_path = generate_report(
        response_data,
        resource_data,
        error_data,
        patterns_data
    )
    
    logger.info("Quarterly performance analysis completed")
    logger.info(f"Report available at: {report_path}")

if __name__ == "__main__":
    main() 