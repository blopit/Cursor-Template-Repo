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

def check_code_complexity():
    """Check code complexity using radon."""
    print("Checking code complexity...")
    try:
        # Get cyclomatic complexity
        cc_result = subprocess.run(
            ["radon", "cc", ".", "--json"],
            capture_output=True,
            text=True
        )
        
        # Get maintainability index
        mi_result = subprocess.run(
            ["radon", "mi", ".", "--json"],
            capture_output=True,
            text=True
        )
        
        return {
            "complexity": json.loads(cc_result.stdout),
            "maintainability": json.loads(mi_result.stdout)
        }
    except FileNotFoundError:
        print("radon not found. Install with: pip install radon")
        return {}

def check_code_duplication():
    """Check for code duplication using pylint."""
    print("\nChecking for code duplication...")
    try:
        result = subprocess.run(
            ["pylint", ".", "--disable=all", "--enable=duplicate-code"],
            capture_output=True,
            text=True
        )
        return result.stdout
    except FileNotFoundError:
        print("pylint not found. Install with: pip install pylint")
        return ""

def check_test_coverage():
    """Check test coverage using pytest-cov."""
    print("\nChecking test coverage...")
    try:
        result = subprocess.run(
            ["pytest", "--cov=.", "--cov-report=json"],
            capture_output=True,
            text=True
        )
        
        if os.path.exists("coverage.json"):
            with open("coverage.json", "r") as f:
                coverage_data = json.load(f)
            os.remove("coverage.json")  # Clean up
            return coverage_data
        return {}
    except FileNotFoundError:
        print("pytest-cov not found. Install with: pip install pytest-cov")
        return {}

def check_documentation_coverage():
    """Check documentation coverage using interrogate."""
    print("\nChecking documentation coverage...")
    try:
        result = subprocess.run(
            ["interrogate", ".", "-v"],
            capture_output=True,
            text=True
        )
        return result.stdout
    except FileNotFoundError:
        print("interrogate not found. Install with: pip install interrogate")
        return ""

def check_style_compliance():
    """Check style compliance using flake8."""
    print("\nChecking style compliance...")
    try:
        result = subprocess.run(
            ["flake8", ".", "--statistics", "--tee"],
            capture_output=True,
            text=True
        )
        return result.stdout
    except FileNotFoundError:
        print("flake8 not found. Install with: pip install flake8")
        return ""

def analyze_complexity_trends(complexity_data: Dict[str, Any]) -> str:
    """Analyze complexity trends and provide recommendations."""
    analysis = []
    
    if not complexity_data:
        return "No complexity data available."
    
    # Analyze cyclomatic complexity
    if "complexity" in complexity_data:
        high_complexity_files = []
        for file_path, metrics in complexity_data["complexity"].items():
            for func in metrics:
                if func["complexity"] > 10:  # High complexity threshold
                    high_complexity_files.append(
                        f"{file_path}::{func['name']} (complexity: {func['complexity']})"
                    )
        
        if high_complexity_files:
            analysis.append("High Complexity Functions:")
            analysis.extend([f"- {f}" for f in high_complexity_files])
    
    # Analyze maintainability
    if "maintainability" in complexity_data:
        low_mi_files = []
        for file_path, mi_score in complexity_data["maintainability"].items():
            if mi_score < 65:  # Low maintainability threshold
                low_mi_files.append(f"{file_path} (MI: {mi_score:.1f})")
        
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
) -> None:
    """Generate a comprehensive code quality report."""
    report_dir = Path(".cursor/logs/code_quality")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"code_quality_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(report_path, "w") as f:
        f.write("Code Quality Report\n")
        f.write("==================\n\n")
        
        # Complexity Analysis
        f.write("Code Complexity\n")
        f.write("--------------\n")
        f.write(analyze_complexity_trends(complexity))
        
        # Duplication
        f.write("\n\nCode Duplication\n")
        f.write("---------------\n")
        f.write(duplication or "No significant code duplication found.")
        
        # Test Coverage
        f.write("\n\nTest Coverage\n")
        f.write("-------------\n")
        if coverage:
            total_coverage = coverage.get("totals", {}).get("percent_covered", 0)
            f.write(f"Overall coverage: {total_coverage:.1f}%\n")
            f.write("\nFiles needing coverage:\n")
            for file_path, metrics in coverage.get("files", {}).items():
                if metrics["summary"]["percent_covered"] < 80:
                    f.write(f"- {file_path}: {metrics['summary']['percent_covered']:.1f}%\n")
        else:
            f.write("No coverage data available.\n")
        
        # Documentation
        f.write("\n\nDocumentation Coverage\n")
        f.write("---------------------\n")
        f.write(documentation or "No documentation coverage data available.")
        
        # Style
        f.write("\n\nStyle Compliance\n")
        f.write("----------------\n")
        f.write(style or "No style issues found.")
        
        # Recommendations
        f.write("\n\nRecommendations\n")
        f.write("---------------\n")
        recommendations = []
        
        if coverage and coverage.get("totals", {}).get("percent_covered", 0) < 80:
            recommendations.append("- Increase test coverage to at least 80%")
        
        if "high complexity" in analyze_complexity_trends(complexity).lower():
            recommendations.append("- Refactor high complexity functions")
        
        if duplication:
            recommendations.append("- Address code duplication issues")
        
        if style:
            recommendations.append("- Fix style compliance issues")
        
        if recommendations:
            f.write("\n".join(recommendations))
        else:
            f.write("No critical issues found. Maintain current quality standards.")

def main():
    print("Running weekly code quality check...")
    
    complexity = check_code_complexity()
    duplication = check_code_duplication()
    coverage = check_test_coverage()
    documentation = check_documentation_coverage()
    style = check_style_compliance()
    
    generate_report(complexity, duplication, coverage, documentation, style)
    
    print("\nCheck complete. Report generated in .cursor/logs/code_quality/")

if __name__ == "__main__":
    main() 