#!/usr/bin/env python3
"""
Quarterly performance analysis script.
Analyzes:
1. Code execution performance
2. Resource usage trends
3. API response times
4. System bottlenecks
5. Historical metrics
"""

import os
import sys
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_historical_metrics() -> pd.DataFrame:
    """Load and combine historical metrics from logs."""
    metrics_dir = Path(".cursor/logs")
    metrics_files = []
    
    # Load dependency check logs
    dep_logs = glob.glob(str(metrics_dir / "dependency_checks/dependency_check_*.txt"))
    for log in dep_logs:
        with open(log, "r") as f:
            date = datetime.strptime(log.split("_")[-1].split(".")[0], "%Y%m%d")
            metrics_files.append({
                "date": date,
                "type": "dependency",
                "content": f.read()
            })
    
    # Load code quality logs
    quality_logs = glob.glob(str(metrics_dir / "code_quality/code_quality_*.txt"))
    for log in quality_logs:
        with open(log, "r") as f:
            date = datetime.strptime(log.split("_")[-1].split(".")[0], "%Y%m%d")
            metrics_files.append({
                "date": date,
                "type": "quality",
                "content": f.read()
            })
    
    # Load security audit logs
    security_logs = glob.glob(str(metrics_dir / "security_audits/security_audit_*.txt"))
    for log in security_logs:
        with open(log, "r") as f:
            date = datetime.strptime(log.split("_")[-1].split(".")[0], "%Y%m%d")
            metrics_files.append({
                "date": date,
                "type": "security",
                "content": f.read()
            })
    
    return pd.DataFrame(metrics_files)

def analyze_performance_trends(metrics_df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze performance trends from historical data."""
    trends = {}
    
    # Analyze frequency of issues
    for metric_type in metrics_df["type"].unique():
        type_data = metrics_df[metrics_df["type"] == metric_type]
        trends[f"{metric_type}_frequency"] = len(type_data) / 90  # Issues per day
    
    # Analyze issue patterns
    for metric_type in metrics_df["type"].unique():
        type_data = metrics_df[metrics_df["type"] == metric_type]
        content_series = type_data["content"].str.lower()
        
        # Count common issues
        trends[f"{metric_type}_issues"] = {
            "errors": content_series.str.count("error").mean(),
            "warnings": content_series.str.count("warning").mean(),
            "critical": content_series.str.count("critical").mean()
        }
    
    return trends

def generate_visualizations(
    metrics_df: pd.DataFrame,
    trends: Dict[str, Any],
    output_dir: Path
) -> None:
    """Generate visualization plots for the analysis."""
    # Set style
    plt.style.use("seaborn")
    
    # Issue Frequency Over Time
    plt.figure(figsize=(12, 6))
    for metric_type in metrics_df["type"].unique():
        type_data = metrics_df[metrics_df["type"] == metric_type]
        plt.plot(type_data["date"], range(len(type_data)), label=metric_type)
    
    plt.title("Cumulative Issues Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Issues")
    plt.legend()
    plt.savefig(output_dir / "issue_frequency.png")
    plt.close()
    
    # Issue Severity Distribution
    plt.figure(figsize=(10, 6))
    severity_data = []
    for metric_type, issues in trends.items():
        if metric_type.endswith("_issues"):
            for severity, count in issues.items():
                severity_data.append({
                    "type": metric_type.replace("_issues", ""),
                    "severity": severity,
                    "count": count
                })
    
    severity_df = pd.DataFrame(severity_data)
    sns.barplot(data=severity_df, x="type", y="count", hue="severity")
    plt.title("Issue Severity Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "severity_distribution.png")
    plt.close()

def analyze_resource_usage():
    """Analyze system resource usage trends."""
    resource_data = {
        "cpu_usage": [],
        "memory_usage": [],
        "disk_usage": []
    }
    
    # This is a placeholder for actual resource monitoring
    # In a real implementation, you would:
    # 1. Collect metrics from your monitoring system
    # 2. Analyze resource usage patterns
    # 3. Identify bottlenecks
    
    return resource_data

def generate_report(
    metrics_df: pd.DataFrame,
    trends: Dict[str, Any],
    resources: Dict[str, List[float]]
) -> None:
    """Generate a comprehensive performance analysis report."""
    report_dir = Path(".cursor/logs/performance_analysis")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Create visualizations directory
    viz_dir = report_dir / "visualizations"
    viz_dir.mkdir(exist_ok=True)
    
    # Generate visualizations
    generate_visualizations(metrics_df, trends, viz_dir)
    
    report_path = report_dir / f"performance_analysis_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(report_path, "w") as f:
        f.write("Quarterly Performance Analysis\n")
        f.write("===========================\n\n")
        
        # Metrics Summary
        f.write("Metrics Summary\n")
        f.write("--------------\n")
        f.write(f"Analysis Period: {metrics_df['date'].min()} to {metrics_df['date'].max()}\n")
        f.write(f"Total Records Analyzed: {len(metrics_df)}\n\n")
        
        # Issue Trends
        f.write("Issue Trends\n")
        f.write("------------\n")
        for metric_type in metrics_df["type"].unique():
            frequency = trends.get(f"{metric_type}_frequency", 0)
            f.write(f"\n{metric_type.title()} Issues:\n")
            f.write(f"- Frequency: {frequency:.2f} issues per day\n")
            
            issues = trends.get(f"{metric_type}_issues", {})
            for severity, count in issues.items():
                f.write(f"- {severity.title()}: {count:.2f} average per report\n")
        
        # Resource Usage
        f.write("\nResource Usage\n")
        f.write("--------------\n")
        for resource, values in resources.items():
            if values:  # Skip empty metrics
                avg_usage = sum(values) / len(values)
                max_usage = max(values)
                f.write(f"\n{resource.replace('_', ' ').title()}:\n")
                f.write(f"- Average: {avg_usage:.2f}%\n")
                f.write(f"- Peak: {max_usage:.2f}%\n")
        
        # Visualizations
        f.write("\nVisualizations\n")
        f.write("--------------\n")
        f.write("Generated visualizations can be found in the 'visualizations' directory:\n")
        f.write("1. issue_frequency.png - Cumulative issues over time\n")
        f.write("2. severity_distribution.png - Distribution of issue severities\n")
        
        # Recommendations
        f.write("\nRecommendations\n")
        f.write("---------------\n")
        recommendations = []
        
        # Analyze issue trends for recommendations
        for metric_type in metrics_df["type"].unique():
            issues = trends.get(f"{metric_type}_issues", {})
            if issues.get("critical", 0) > 1:
                recommendations.append(
                    f"- Address high number of critical {metric_type} issues"
                )
            if issues.get("errors", 0) > 5:
                recommendations.append(
                    f"- Investigate frequent {metric_type} errors"
                )
        
        # Resource-based recommendations
        for resource, values in resources.items():
            if values and max(values) > 80:  # High resource usage
                recommendations.append(
                    f"- Optimize {resource.replace('_', ' ')} usage"
                )
        
        if recommendations:
            f.write("\n".join(recommendations))
        else:
            f.write("No critical performance issues identified. Continue monitoring.")

def main():
    print("Running quarterly performance analysis...")
    
    # Load historical data
    metrics_df = load_historical_metrics()
    
    # Analyze trends
    trends = analyze_performance_trends(metrics_df)
    
    # Analyze resource usage
    resources = analyze_resource_usage()
    
    # Generate report
    generate_report(metrics_df, trends, resources)
    
    print("\nAnalysis complete. Report generated in .cursor/logs/performance_analysis/")

if __name__ == "__main__":
    main() 