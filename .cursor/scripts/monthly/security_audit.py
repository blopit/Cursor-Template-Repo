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

def check_dependencies_security():
    """Check for known vulnerabilities using safety."""
    print("Checking for known vulnerabilities...")
    try:
        result = subprocess.run(
            ["safety", "check", "--json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.stdout else {}
    except FileNotFoundError:
        print("safety not found. Install with: pip install safety")
        return {}

def scan_for_secrets():
    """Scan for hardcoded secrets using detect-secrets."""
    print("\nScanning for hardcoded secrets...")
    try:
        result = subprocess.run(
            ["detect-secrets", "scan", "."],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.stdout else {}
    except FileNotFoundError:
        print("detect-secrets not found. Install with: pip install detect-secrets")
        return {}

def check_security_patterns():
    """Check for security anti-patterns using bandit."""
    print("\nChecking for security anti-patterns...")
    try:
        result = subprocess.run(
            ["bandit", "-r", ".", "-f", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.stdout else {}
    except FileNotFoundError:
        print("bandit not found. Install with: pip install bandit")
        return {}

def check_api_key_rotation():
    """Check API key age and rotation needs."""
    print("\nChecking API key rotation needs...")
    rotation_data = {}
    
    # Check .env file modification time
    if os.path.exists(".env"):
        env_stat = os.stat(".env")
        last_modified = datetime.fromtimestamp(env_stat.st_mtime)
        days_old = (datetime.now() - last_modified).days
        
        rotation_data["env_file"] = {
            "last_modified": last_modified.isoformat(),
            "days_old": days_old,
            "needs_rotation": days_old > 90  # Recommend rotation after 90 days
        }
    
    return rotation_data

def analyze_security_findings(
    vulnerabilities: Dict[str, Any],
    secrets: Dict[str, Any],
    patterns: Dict[str, Any],
    rotation: Dict[str, Any]
) -> List[str]:
    """Analyze security findings and generate recommendations."""
    recommendations = []
    
    # Analyze vulnerabilities
    if vulnerabilities:
        for vuln in vulnerabilities:
            recommendations.append(
                f"- Update {vuln.get('package')}: {vuln.get('description')}"
            )
    
    # Analyze secrets
    if secrets.get("results"):
        for file_path, secret_list in secrets["results"].items():
            if secret_list:
                recommendations.append(
                    f"- Remove hardcoded secrets from {file_path}"
                )
    
    # Analyze security patterns
    if patterns.get("results"):
        for result in patterns["results"]:
            if result.get("issue_severity") in ("HIGH", "MEDIUM"):
                recommendations.append(
                    f"- Fix {result.get('issue_text')} in {result.get('filename')}"
                )
    
    # Analyze key rotation
    if rotation.get("env_file", {}).get("needs_rotation"):
        recommendations.append(
            "- Rotate API keys (last rotation: "
            f"{rotation['env_file']['days_old']} days ago)"
        )
    
    return recommendations

def generate_report(
    vulnerabilities: Dict[str, Any],
    secrets: Dict[str, Any],
    patterns: Dict[str, Any],
    rotation: Dict[str, Any]
) -> None:
    """Generate a comprehensive security audit report."""
    report_dir = Path(".cursor/logs/security_audits")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"security_audit_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(report_path, "w") as f:
        f.write("Security Audit Report\n")
        f.write("===================\n\n")
        
        # Dependency Vulnerabilities
        f.write("Known Vulnerabilities\n")
        f.write("--------------------\n")
        if vulnerabilities:
            for vuln in vulnerabilities:
                f.write(f"Package: {vuln.get('package')}\n")
                f.write(f"Severity: {vuln.get('severity')}\n")
                f.write(f"Description: {vuln.get('description')}\n\n")
        else:
            f.write("No known vulnerabilities found.\n")
        
        # Hardcoded Secrets
        f.write("\nHardcoded Secrets\n")
        f.write("-----------------\n")
        if secrets.get("results"):
            for file_path, secret_list in secrets["results"].items():
                if secret_list:
                    f.write(f"\nFile: {file_path}\n")
                    f.write(f"Found {len(secret_list)} potential secrets\n")
        else:
            f.write("No hardcoded secrets found.\n")
        
        # Security Anti-patterns
        f.write("\nSecurity Anti-patterns\n")
        f.write("---------------------\n")
        if patterns.get("results"):
            for result in patterns["results"]:
                f.write(f"\nIssue: {result.get('issue_text')}\n")
                f.write(f"Severity: {result.get('issue_severity')}\n")
                f.write(f"File: {result.get('filename')}\n")
                f.write(f"Line: {result.get('line_number')}\n")
        else:
            f.write("No security anti-patterns found.\n")
        
        # API Key Rotation
        f.write("\nAPI Key Rotation\n")
        f.write("---------------\n")
        if rotation.get("env_file"):
            f.write(f"Last modified: {rotation['env_file']['last_modified']}\n")
            f.write(f"Days since last rotation: {rotation['env_file']['days_old']}\n")
            if rotation['env_file']['needs_rotation']:
                f.write("WARNING: API keys should be rotated\n")
        else:
            f.write("No API keys found for rotation check.\n")
        
        # Recommendations
        f.write("\nSecurity Recommendations\n")
        f.write("----------------------\n")
        recommendations = analyze_security_findings(
            vulnerabilities, secrets, patterns, rotation
        )
        if recommendations:
            f.write("\n".join(recommendations))
        else:
            f.write("No critical security issues found. Maintain current security standards.")

def main():
    print("Running monthly security audit...")
    
    vulnerabilities = check_dependencies_security()
    secrets = scan_for_secrets()
    patterns = check_security_patterns()
    rotation = check_api_key_rotation()
    
    generate_report(vulnerabilities, secrets, patterns, rotation)
    
    print("\nAudit complete. Report generated in .cursor/logs/security_audits/")

if __name__ == "__main__":
    main() 