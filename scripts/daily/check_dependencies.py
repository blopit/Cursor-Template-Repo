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
from typing import Dict, List, Any

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
    """Check for dependency conflicts using pipdeptree."""
    try:
        result = subprocess.run(
            ['pipdeptree', '--json-tree', '--warn', 'silence'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse pipdeptree output to find conflicts
        tree_data = json.loads(result.stdout)
        conflicts = []
        
        for package in tree_data:
            package_conflicts = []
            for dependency in package.get("dependencies", []):
                if dependency.get("required_version") and \
                   dependency.get("installed_version") and \
                   not _version_satisfies_requirement(
                       dependency["installed_version"],
                       dependency["required_version"]
                   ):
                    package_conflicts.append({
                        "package": dependency["key"],
                        "required_version": dependency["required_version"],
                        "installed_version": dependency["installed_version"]
                    })
            
            if package_conflicts:
                conflicts.append({
                    "package": package["package"]["key"],
                    "current_version": package["package"]["installed_version"],
                    "conflicting_deps": package_conflicts
                })
        
        return {"conflicts": conflicts}
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking dependency conflicts: {str(e)}")
        return {}

def check_unused_dependencies() -> Dict[str, List[Dict[str, Any]]]:
    """Check for unused dependencies using pipreqs."""
    try:
        # First, get list of all installed packages
        installed = subprocess.run(
            ['pip', 'list', '--format=json'],
            capture_output=True,
            text=True,
            check=True
        )
        installed_packages = {
            pkg["name"]: pkg["version"]
            for pkg in json.loads(installed.stdout)
        }
        
        # Then, get list of required packages
        result = subprocess.run(
            ['pipreqs', '.', '--print'],
            capture_output=True,
            text=True,
            check=True
        )
        
        required_packages = set()
        for line in result.stdout.splitlines():
            if '==' in line:
                package = line.split('==')[0]
                required_packages.add(package.lower())
        
        # Find unused packages
        unused = []
        for package, version in installed_packages.items():
            if package.lower() not in required_packages:
                # Get package size
                size = subprocess.run(
                    ['pip', 'show', package],
                    capture_output=True,
                    text=True
                )
                size_info = "unknown"
                for line in size.stdout.splitlines():
                    if line.startswith("Size:"):
                        size_info = line.split(":")[1].strip()
                        break
                
                unused.append({
                    "package": package,
                    "version": version,
                    "size": size_info
                })
        
        return {"unused": unused}
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking unused dependencies: {str(e)}")
        return {}

def check_package_licenses() -> Dict[str, List[Dict[str, Any]]]:
    """Check package licenses using pip-licenses."""
    try:
        result = subprocess.run(
            ['pip-licenses', '--format=json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        licenses_data = json.loads(result.stdout)
        approved_licenses = {
            'MIT', 'Apache-2.0', 'BSD-3-Clause', 'BSD-2-Clause',
            'ISC', 'Python-2.0', 'MPL-2.0'
        }
        
        licenses = []
        for pkg in licenses_data:
            licenses.append({
                "package": pkg["Name"],
                "version": pkg["Version"],
                "license": pkg["License"],
                "approved": pkg["License"] in approved_licenses
            })
        
        return {"licenses": licenses}
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking package licenses: {str(e)}")
        return {}

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
    outdated_data: Dict[str, List[Dict[str, Any]]],
    conflicts_data: Dict[str, List[Dict[str, Any]]],
    unused_data: Dict[str, List[Dict[str, Any]]],
    license_data: Dict[str, List[Dict[str, Any]]]
) -> Path:
    """Generate a comprehensive dependency check report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path(".cursor") / "logs" / "dependency_checks"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = log_dir / f"dependency_check_{timestamp}.txt"
    
    with open(report_path, 'w') as f:
        f.write("=== Dependency Check Report ===\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Outdated Packages
        f.write("=== Outdated Packages ===\n")
        if outdated_data.get("outdated"):
            for pkg in outdated_data["outdated"]:
                f.write(
                    f"Package: {pkg['name']}\n"
                    f"Current Version: {pkg['current_version']}\n"
                    f"Latest Version: {pkg['latest_version']}\n"
                    f"Update Type: {pkg.get('type', 'unknown')}\n\n"
                )
        else:
            f.write("No outdated packages found.\n\n")
        
        # Dependency Conflicts
        f.write("=== Dependency Conflicts ===\n")
        if conflicts_data.get("conflicts"):
            for conflict in conflicts_data["conflicts"]:
                f.write(
                    f"Package: {conflict['package']}\n"
                    f"Version: {conflict.get('current_version', 'unknown')}\n"
                    f"Conflicting Dependencies:\n"
                )
                for dep in conflict.get("conflicting_deps", []):
                    f.write(
                        f"  - {dep['package']}\n"
                        f"    Required: {dep['required_version']}\n"
                        f"    Installed: {dep['installed_version']}\n"
                    )
                f.write("\n")
        else:
            f.write("No dependency conflicts found.\n\n")
        
        # Unused Dependencies
        f.write("=== Unused Dependencies ===\n")
        if unused_data.get("unused"):
            for pkg in unused_data["unused"]:
                f.write(
                    f"Package: {pkg['package']}\n"
                    f"Version: {pkg['version']}\n"
                    f"Size: {pkg['size']}\n\n"
                )
        else:
            f.write("No unused dependencies found.\n\n")
        
        # Package Licenses
        f.write("=== Package Licenses ===\n")
        if license_data.get("licenses"):
            unapproved_licenses = []
            for pkg in license_data["licenses"]:
                if not pkg.get("approved", True):
                    unapproved_licenses.append(
                        f"Package: {pkg['package']}\n"
                        f"Version: {pkg['version']}\n"
                        f"License: {pkg['license']}\n"
                    )
            
            if unapproved_licenses:
                f.write("Packages with Unapproved Licenses:\n")
                f.write("\n".join(unapproved_licenses))
            else:
                f.write("All package licenses are approved.\n")
        else:
            f.write("No license information available.\n\n")
        
        # Dependency Analysis
        f.write("=== Dependency Analysis ===\n")
        f.write(analyze_dependency_trends({
            "outdated": outdated_data.get("outdated", []),
            "conflicts": conflicts_data.get("conflicts", [])
        }))
    
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
        outdated_data,
        conflicts_data,
        unused_data,
        license_data
    )
    
    logger.info("Daily dependency check completed")
    logger.info(f"Report available at: {report_path}")

if __name__ == "__main__":
    main() 