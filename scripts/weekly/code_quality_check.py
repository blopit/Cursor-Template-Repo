#!/usr/bin/env python3
"""
Weekly code quality checker script.
Checks for:
1. Code complexity
2. Code duplication
3. Test coverage
4. Documentation coverage
5. Style compliance
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

def check_code_complexity():
    """Check code complexity using radon."""
    logger.info("Checking code complexity...")
    try:
        # Get cyclomatic complexity
        complexity_result = subprocess.run(
            ['radon', 'cc', '.', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get maintainability index
        maintainability_result = subprocess.run(
            ['radon', 'mi', '.', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            "complexity": json.loads(complexity_result.stdout),
            "maintainability": json.loads(maintainability_result.stdout)
        }
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking code complexity: {str(e)}")
        return {}

def check_code_duplication():
    """Check for code duplication using CPD."""
    logger.info("\nChecking for code duplication...")
    try:
        result = subprocess.run(
            ['cpd', '--minimum-tokens', '100', '--files', '.'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking code duplication: {str(e)}")
        return "Error checking code duplication"

def check_test_coverage():
    """Check test coverage using pytest-cov."""
    logger.info("\nChecking test coverage...")
    coverage_file = Path('.coverage')
    if not os.path.exists(coverage_file):
        try:
            subprocess.run(
                ['pytest', '--cov=.', '--cov-report=json'],
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Error running test coverage: {str(e)}")
            return {}
    
    try:
        with open('coverage.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error reading coverage data: {str(e)}")
        return {}

def check_documentation_coverage():
    """Check documentation coverage using pydocstyle."""
    logger.info("\nChecking documentation coverage...")
    try:
        result = subprocess.run(
            ['pydocstyle', '.'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking documentation: {str(e)}")
        return "Error checking documentation coverage"

def check_style_compliance():
    """Check style compliance using flake8."""
    logger.info("\nChecking style compliance...")
    try:
        result = subprocess.run(
            ['flake8', '.', '--max-line-length=100'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking style compliance: {str(e)}")
        return "Error checking style compliance"

def analyze_complexity_trends(complexity_data: Dict[str, Any]) -> str:
    """Analyze complexity trends and provide recommendations."""
    analysis = []
    
    if not complexity_data:
        return "No complexity data available."
    
    # Analyze cyclomatic complexity
    if "complexity" in complexity_data:
        high_complexity_files = []
        for file_path, functions in complexity_data["complexity"].items():
            for func in functions:
                if func.get("complexity", 0) > 10:  # High complexity threshold
                    high_complexity_files.append(
                        f"{file_path}::{func['name']} - "
                        f"complexity: {func['complexity']} "
                        f"(line {func.get('line_number', 'unknown')})"
                    )
        
        if high_complexity_files:
            analysis.append("High Complexity Functions:")
            analysis.extend([f"- {f}" for f in high_complexity_files])
    
    # Analyze maintainability
    if "maintainability" in complexity_data:
        low_mi_files = []
        for file_path, mi_score in complexity_data["maintainability"].items():
            if mi_score < 65:  # Low maintainability threshold
                low_mi_files.append(f"{file_path} - MI: {mi_score}")
        
        if low_mi_files:
            analysis.append("\nLow Maintainability Files:")
            analysis.extend([f"- {f}" for f in low_mi_files])
    
    return "\n".join(analysis) if analysis else "All files within acceptable complexity limits."

def generate_report(
    complexity: Dict[str, Any],
    duplication: str,
    coverage: Dict[str, Any],
    documentation: str,
    style: str
) -> Path:
    """Generate a comprehensive code quality report.
    
    Returns:
        Path: The path to the generated report file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path(".cursor") / "logs" / "code_quality"
    log_dir.mkdir(parents=True, exist_ok=True)

    report_path = log_dir / f"quality_report_{timestamp}.txt"
    
    report_content = [
        "Code Quality Report",
        "=================",
        f"\nTimestamp: {timestamp}\n",
        "\nComplexity Analysis:",
        "-------------------"
    ]
    
    # Add complexity details
    for file_path, funcs in complexity.get("complexity", {}).items():
        report_content.append(f"\nFile: {file_path}")
        for func in funcs:
            report_content.append(f"- {func['name']} (complexity: {func['complexity']})")
    
    # Add maintainability
    report_content.extend([
        "\nMaintainability Index:",
        "--------------------"
    ])
    for file_path, index in complexity.get("maintainability", {}).items():
        report_content.append(f"\nFile: {file_path} - Index: {index:.1f}")
    
    # Add duplication info
    report_content.extend([
        "\nCode Duplication:",
        "----------------",
        f"\n{duplication}"
    ])
    
    # Add coverage info
    report_content.extend([
        "\nCode Coverage:",
        "--------------",
        f"\nTotal coverage: {coverage['totals']['percent_covered']}%"
    ])
    
    # Add documentation coverage
    report_content.extend([
        "\nDocumentation:",
        "--------------",
        f"\n{documentation}"
    ])
    
    # Add style issues
    report_content.extend([
        "\nStyle Check:",
        "------------",
        f"\n{style}"
    ])
    
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_content))
    
    return report_path

def main():
    """Run all code quality checks and generate report."""
    logger.info("Starting weekly code quality check...")
    
    complexity = check_code_complexity()
    logger.info("Completed complexity check")
    
    duplication = check_code_duplication()
    logger.info("Completed duplication check")
    
    coverage = check_test_coverage()
    logger.info("Completed coverage check")
    
    documentation = check_documentation_coverage()
    logger.info("Completed documentation check")
    
    style = check_style_compliance()
    logger.info("Completed style check")
    
    report_path = generate_report(
        complexity,
        duplication,
        coverage,
        documentation,
        style
    )
    
    logger.info("Weekly code quality check completed")
    logger.info(f"Report available at: {report_path}")

if __name__ == "__main__":
    main() 