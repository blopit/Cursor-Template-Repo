#!/usr/bin/env python3
"""
Monthly security audit script.
Checks for:
1. Known vulnerabilities in dependencies
2. Hardcoded secrets
3. Security anti-patterns
4. Outdated security packages
5. API key rotation needs
"""

import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependency_vulnerabilities() -> Dict[str, List[Dict[str, Any]]]:
    """Check for known vulnerabilities in dependencies using safety."""
    try:
        result = subprocess.run(
            ['safety', 'check', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking dependencies: {str(e)}")
        return {}

def check_secrets_exposure() -> Dict[str, List[Dict[str, Any]]]:
    """Check for exposed secrets using detect-secrets."""
    try:
        result = subprocess.run(
            ['detect-secrets', 'scan', '--all-files', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking for secrets: {str(e)}")
        return {}

def check_security_patterns() -> Dict[str, List[Dict[str, Any]]]:
    """Check for common security anti-patterns using bandit."""
    try:
        result = subprocess.run(
            ['bandit', '-r', '.', '-f', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error checking security patterns: {str(e)}")
        return {}

def check_api_key_rotation() -> Dict[str, List[Dict[str, Any]]]:
    """Check API key rotation dates from comments in configuration files."""
    api_keys = []
    rotation_pattern = re.compile(r'API_KEY.*?#.*?Last rotated: (\d{4}-\d{2}-\d{2})')
    
    try:
        config_files = Path('.').glob('**/*.py')
        for file in config_files:
            if file.is_file():
                content = file.read_text()
                matches = rotation_pattern.findall(content)
                if matches:
                    for last_rotation in matches:
                        api_keys.append({
                            "file": str(file),
                            "last_rotation": last_rotation
                        })
    except Exception as e:
        logger.error(f"Error checking API key rotation: {str(e)}")
    
    return {"api_keys": api_keys}

def analyze_security_trends(security_data: Dict[str, Any]) -> str:
    """Analyze trends in security scan data."""
    analysis = []
    
    # Analyze vulnerabilities
    analysis.append("High Severity Vulnerabilities:")
    for vuln in security_data.get("vulnerabilities", []):
        if vuln.get("severity") == "HIGH":
            analysis.append(
                f"{vuln['package']} {vuln['version']} - "
                f"{vuln.get('description', 'No description')} "
                f"(Fix version: {vuln.get('fix_version', 'unknown')})"
            )
    
    # Analyze exposed secrets
    analysis.append("\nExposed Secrets:")
    for secret in security_data.get("secrets", []):
        analysis.append(
            f"{secret['file']}:{secret.get('line', 'unknown')} - "
            f"Type: {secret.get('type', 'unknown')} "
            f"(Severity: {secret.get('severity', 'unknown')})"
        )
    
    return "\n".join(analysis)

def generate_report(
    vulnerability_data: Dict[str, List[Dict[str, Any]]],
    secrets_data: Dict[str, List[Dict[str, Any]]],
    patterns_data: Dict[str, List[Dict[str, Any]]],
    api_keys_data: Dict[str, List[Dict[str, Any]]]
) -> Path:
    """Generate a comprehensive security audit report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path(".cursor") / "logs" / "security_audits"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = log_dir / f"security_audit_{timestamp}.txt"
    
    with open(report_path, 'w') as f:
        f.write("=== Security Audit Report ===\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Dependency Vulnerabilities
        f.write("=== Dependency Vulnerabilities ===\n")
        if vulnerability_data.get("vulnerabilities"):
            for vuln in vulnerability_data["vulnerabilities"]:
                f.write(
                    f"Package: {vuln['package']} {vuln['version']}\n"
                    f"Severity: {vuln.get('severity', 'unknown')}\n"
                    f"Description: {vuln.get('description', 'No description')}\n"
                    f"Fix Version: {vuln.get('fix_version', 'unknown')}\n\n"
                )
        else:
            f.write("No vulnerabilities found.\n\n")
        
        # Exposed Secrets
        f.write("=== Exposed Secrets ===\n")
        if secrets_data.get("exposed_secrets"):
            for secret in secrets_data["exposed_secrets"]:
                f.write(
                    f"File: {secret['file']}\n"
                    f"Line: {secret.get('line', 'unknown')}\n"
                    f"Type: {secret.get('type', 'unknown')}\n"
                    f"Severity: {secret.get('severity', 'unknown')}\n\n"
                )
        else:
            f.write("No exposed secrets found.\n\n")
        
        # Security Patterns
        f.write("=== Security Anti-patterns ===\n")
        if patterns_data.get("issues"):
            for issue in patterns_data["issues"]:
                f.write(
                    f"File: {issue['file']}\n"
                    f"Line: {issue.get('line', 'unknown')}\n"
                    f"Pattern: {issue['pattern']}\n"
                    f"Severity: {issue.get('severity', 'unknown')}\n\n"
                )
        else:
            f.write("No security anti-patterns found.\n\n")
        
        # API Key Rotation
        f.write("=== API Key Rotation ===\n")
        if api_keys_data.get("api_keys"):
            for key in api_keys_data["api_keys"]:
                f.write(
                    f"File: {key['file']}\n"
                    f"Last Rotation: {key['last_rotation']}\n\n"
                )
        else:
            f.write("No API keys found or no rotation dates specified.\n\n")
        
        # Security Analysis
        f.write("=== Security Analysis ===\n")
        f.write(analyze_security_trends({
            "vulnerabilities": vulnerability_data.get("vulnerabilities", []),
            "secrets": secrets_data.get("exposed_secrets", [])
        }))
    
    logger.info(f"Report generated: {report_path}")
    return report_path

def main():
    """Run monthly security audit checks."""
    logger.info("Starting monthly security audit...")
    
    vulnerability_data = check_dependency_vulnerabilities()
    logger.info("Completed dependency vulnerability check")
    
    secrets_data = check_secrets_exposure()
    logger.info("Completed secrets exposure check")
    
    patterns_data = check_security_patterns()
    logger.info("Completed security patterns check")
    
    api_keys_data = check_api_key_rotation()
    logger.info("Completed API key rotation check")
    
    report_path = generate_report(
        vulnerability_data,
        secrets_data,
        patterns_data,
        api_keys_data
    )
    
    logger.info("Monthly security audit completed")
    logger.info(f"Report available at: {report_path}")

if __name__ == "__main__":
    main() 