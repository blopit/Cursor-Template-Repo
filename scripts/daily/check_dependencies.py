#!/usr/bin/env python3
"""
Daily dependency checker script.
Checks for:
1. Outdated packages
2. Unused imports
3. Missing requirements
4. Dependency conflicts
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

def check_outdated_packages():
    """Check for outdated packages using pip-outdated."""
    print("Checking for outdated packages...")
    try:
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True
        )
        outdated = json.loads(result.stdout)
        if outdated:
            print("\nOutdated packages:")
            for pkg in outdated:
                print(f"- {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        return outdated
    except Exception as e:
        print(f"Error checking outdated packages: {e}")
        return []

def find_unused_imports():
    """Find unused imports using vulture."""
    print("\nChecking for unused imports...")
    try:
        result = subprocess.run(
            ["vulture", "."],
            capture_output=True,
            text=True
        )
        if result.stdout:
            print("\nPotentially unused code:")
            print(result.stdout)
        return result.stdout
    except FileNotFoundError:
        print("vulture not found. Install with: pip install vulture")
        return ""

def check_missing_requirements():
    """Check for imports not in requirements.txt."""
    print("\nChecking for missing requirements...")
    try:
        # Get installed packages
        result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True
        )
        installed = {
            line.split("==")[0].lower()
            for line in result.stdout.splitlines()
        }
        
        # Get requirements
        with open("requirements.txt", "r") as f:
            requirements = {
                line.split(">=")[0].split("==")[0].strip().lower()
                for line in f.readlines()
                if line.strip() and not line.startswith("#")
            }
        
        # Find missing
        missing = installed - requirements
        if missing:
            print("\nPackages not in requirements.txt:")
            for pkg in sorted(missing):
                print(f"- {pkg}")
        return missing
    except Exception as e:
        print(f"Error checking missing requirements: {e}")
        return set()

def check_dependency_conflicts():
    """Check for dependency conflicts using pipdeptree."""
    print("\nChecking for dependency conflicts...")
    try:
        result = subprocess.run(
            ["pipdeptree", "--warn", "silence"],
            capture_output=True,
            text=True
        )
        if "Warning" in result.stdout:
            print("\nDependency conflicts found:")
            print(result.stdout)
        return result.stdout
    except FileNotFoundError:
        print("pipdeptree not found. Install with: pip install pipdeptree")
        return ""

def generate_report(outdated, unused, missing, conflicts):
    """Generate a report of all findings."""
    report_dir = Path(".cursor/logs/dependency_checks")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"dependency_check_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(report_path, "w") as f:
        f.write("Dependency Check Report\n")
        f.write("======================\n\n")
        
        f.write("Outdated Packages\n")
        f.write("-----------------\n")
        for pkg in outdated:
            f.write(f"{pkg['name']}: {pkg['version']} → {pkg['latest_version']}\n")
        
        f.write("\nUnused Imports\n")
        f.write("-------------\n")
        f.write(unused)
        
        f.write("\nMissing from requirements.txt\n")
        f.write("--------------------------\n")
        for pkg in missing:
            f.write(f"{pkg}\n")
        
        f.write("\nDependency Conflicts\n")
        f.write("-------------------\n")
        f.write(conflicts)

def main():
    print("Running daily dependency check...")
    
    outdated = check_outdated_packages()
    unused = find_unused_imports()
    missing = check_missing_requirements()
    conflicts = check_dependency_conflicts()
    
    generate_report(outdated, unused, missing, conflicts)
    
    print("\nCheck complete. Report generated in .cursor/logs/dependency_checks/")

if __name__ == "__main__":
    main() 