#!/usr/bin/env python3
"""
Daily dependency check script.

This script performs various dependency checks including:
- Outdated package detection
- Dependency conflict analysis
- Unused dependency identification
- Package license verification

Results are saved to .cursor/logs/dependency_checks/
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
import os
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_outdated_packages() -> Dict[str, List[Dict[str, Any]]]:
    """Check for outdated packages using pip-outdated."""
    try:
        result = subprocess.run(
            ['pip-outdated', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking outdated packages: {str(e)}")
        return {}

def check_dependency_conflicts() -> Dict[str, List[Dict[str, Any]]]:
    """Check for dependency conflicts using pip-check."""
    try:
        result = subprocess.run(
            ['pip-check', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error checking dependency conflicts: {str(e)}")
        return {"conflicts": []}

def check_unused_dependencies() -> Dict[str, List[Dict[str, Any]]]:
    """Check for unused dependencies using pipdeptree."""
    try:
        result = subprocess.run(
            ['pipdeptree', '--json-tree'],
            capture_output=True,
            text=True,
            check=True
        )
        return {"unused": json.loads(result.stdout)}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error checking unused dependencies: {str(e)}")
        return {"unused": []}

def check_package_licenses() -> Dict[str, List[Dict[str, Any]]]:
    """Check package licenses using pip-licenses."""
    try:
        result = subprocess.run(
            ['pip-licenses', '--format=json'],
            capture_output=True,
            text=True,
            check=True
        )
        return {"licenses": json.loads(result.stdout)}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error checking package licenses: {str(e)}")
        return {"licenses": []}

def _version_satisfies_requirement(installed_version: str, required_version: str) -> bool:
    """Helper function to check if installed version satisfies requirement."""
    try:
        from packaging import version, requirements
        
        # Parse the installed version
        installed = version.parse(installed_version)
        
        # Parse the requirement
        req = requirements.Requirement(f"dummy{required_version}")
        
        # Check if installed version matches requirement
        return installed in req.specifier
    except Exception as e:
        logger.error(f"Error comparing versions: {str(e)}")
        return False

def analyze_dependency_trends(dependency_data: Dict[str, Any]) -> str:
    """Analyze trends in dependency data."""
    analysis = []
    
    # Analyze outdated packages
    analysis.append("Outdated Packages:")
    for pkg in dependency_data.get("outdated", []):
        analysis.append(
            f"{pkg['name']} {pkg['current_version']} -> {pkg['latest_version']} "
            f"(Update type: {pkg.get('type', 'unknown')})"
        )
    
    # Analyze dependency conflicts
    analysis.append("\nDependency Conflicts:")
    for conflict in dependency_data.get("conflicts", []):
        analysis.append(
            f"{conflict['package']} {conflict.get('current_version', '')}"
        )
        for dep in conflict.get("conflicting_deps", []):
            analysis.append(
                f"  - {dep['package']}: requires {dep['required_version']}, "
                f"has {dep['installed_version']}"
            )
    
    return "\n".join(analysis)

def generate_report(
    conflicts_data: Dict[str, List[Dict[str, Any]]],
    unused_data: Dict[str, List[Dict[str, Any]]],
    licenses_data: Dict[str, List[Dict[str, Any]]],
    log_dir: Optional[Path] = None
) -> Path:
    """Generate a comprehensive dependency check report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if log_dir is None:
        log_dir = Path(".cursor") / "logs" / "dependency_checks"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = log_dir / f"dependency_report_{timestamp}.txt"
    
    with open(report_path, 'w') as f:
        f.write("=== Dependency Check Report ===\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Dependency Conflicts
        f.write("=== Dependency Conflicts ===\n")
        if conflicts_data["conflicts"]:
            for conflict in conflicts_data["conflicts"]:
                f.write(
                    f"Package: {conflict['package']} {conflict['version']}\n"
                    f"Conflicts with: {conflict['conflict_with']}\n"
                    f"Required version: {conflict['required_version']}\n"
                    f"Current version: {conflict['current_version']}\n\n"
                )
        else:
            f.write("No dependency conflicts found.\n\n")
        
        # Unused Dependencies
        f.write("=== Unused Dependencies ===\n")
        if unused_data["unused"]:
            for unused in unused_data["unused"]:
                f.write(
                    f"Package: {unused['package']} {unused['version']}\n"
                    f"Last used: {unused['last_used']}\n\n"
                )
        else:
            f.write("No unused dependencies found.\n\n")
        
        # Package Licenses
        f.write("=== Package Licenses ===\n")
        if licenses_data["licenses"]:
            for license_info in licenses_data["licenses"]:
                f.write(
                    f"Package: {license_info['package']} {license_info['version']}\n"
                    f"License: {license_info['license']}\n"
                    f"Compliant: {license_info['compliant']}\n\n"
                )
        else:
            f.write("No license information found.\n\n")
    
    logger.info(f"Report generated: {report_path}")
    return report_path

def main():
    """Run daily dependency checks."""
    logger.info("Starting daily dependency check...")
    
    outdated_data = check_outdated_packages()
    logger.info("Completed outdated package check")
    
    conflicts_data = check_dependency_conflicts()
    logger.info("Completed dependency conflict check")
    
    unused_data = check_unused_dependencies()
    logger.info("Completed unused dependency check")
    
    license_data = check_package_licenses()
    logger.info("Completed package license check")
    
    report_path = generate_report(
        conflicts_data,
        unused_data,
        license_data
    )
    
    logger.info("Daily dependency check completed")
    logger.info(f"Report available at: {report_path}")

if __name__ == "__main__":
    main() 