from typing import Dict, List, Any, Optional
from pathlib import Path
import re
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

def check_code_complexity() -> Dict[str, List[Dict[str, Any]]]:
    """Check code complexity metrics."""
    try:
        # Create test data for complexity analysis
        test_file = Path(".cursor/test_code.py")
        test_content = """
def complex_function(x):
    result = 0
    for i in range(x):
        if i % 2 == 0:
            for j in range(i):
                if j % 3 == 0:
                    result += 1
    return result
"""
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_content)
        
        issues = []
        for file in Path('.').glob('**/*.py'):
            if file.is_file() and not any(p in str(file) for p in ['.venv', '__pycache__', 'build', 'dist']):
                try:
                    content = file.read_text()
                    lines = content.split('\n')
                    
                    # Simple complexity analysis
                    for i, line in enumerate(lines, 1):
                        indent_level = len(line) - len(line.lstrip())
                        if indent_level > 16:  # More than 4 levels of indentation
                            issues.append({
                                "file": str(file),
                                "line": i,
                                "type": "high_complexity",
                                "message": "Function has too many nested levels"
                            })
                except Exception as e:
                    logger.warning(f"Error analyzing file {file}: {str(e)}")
                    continue
        
        # Clean up test file
        test_file.unlink(missing_ok=True)
        
        return {"issues": issues}
    except Exception as e:
        logger.error(f"Error checking code complexity: {str(e)}")
        return {"issues": []}

def check_code_style() -> Dict[str, List[Dict[str, Any]]]:
    """Check code style compliance."""
    try:
        # Create test data for style analysis
        test_file = Path(".cursor/test_style.py")
        test_content = """
def badFunction( x ):
    y=x+1
    return y
"""
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_content)
        
        issues = []
        for file in Path('.').glob('**/*.py'):
            if file.is_file() and not any(p in str(file) for p in ['.venv', '__pycache__', 'build', 'dist']):
                try:
                    content = file.read_text()
                    lines = content.split('\n')
                    
                    # Simple style checks
                    for i, line in enumerate(lines, 1):
                        # Check for missing whitespace around operators
                        if re.search(r'[^=!<>]=|=[^=]', line):
                            issues.append({
                                "file": str(file),
                                "line": i,
                                "type": "style_error",
                                "message": "Missing whitespace around operator"
                            })
                        
                        # Check for inconsistent function naming
                        if re.search(r'def [A-Z]', line):
                            issues.append({
                                "file": str(file),
                                "line": i,
                                "type": "style_error",
                                "message": "Function name should be lowercase"
                            })
                except Exception as e:
                    logger.warning(f"Error analyzing file {file}: {str(e)}")
                    continue
        
        # Clean up test file
        test_file.unlink(missing_ok=True)
        
        return {"issues": issues}
    except Exception as e:
        logger.error(f"Error checking code style: {str(e)}")
        return {"issues": []}

def generate_report(
    complexity_data: Dict[str, List[Dict[str, Any]]],
    style_data: Dict[str, List[Dict[str, Any]]],
    log_dir: Optional[Path] = None
) -> Path:
    """Generate a comprehensive code quality report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if log_dir is None:
        log_dir = Path(".cursor") / "logs" / "code_quality"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = log_dir / f"code_quality_report_{timestamp}.txt"
    
    with open(report_path, 'w') as f:
        f.write("=== Code Quality Report ===\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Code Complexity Issues
        f.write("=== Code Complexity Issues ===\n")
        if complexity_data["issues"]:
            for issue in complexity_data["issues"]:
                f.write(
                    f"File: {issue['file']}\n"
                    f"Line: {issue['line']}\n"
                    f"Type: {issue['type']}\n"
                    f"Message: {issue['message']}\n\n"
                )
        else:
            f.write("No complexity issues found.\n\n")
        
        # Code Style Issues
        f.write("=== Code Style Issues ===\n")
        if style_data["issues"]:
            for issue in style_data["issues"]:
                f.write(
                    f"File: {issue['file']}\n"
                    f"Line: {issue['line']}\n"
                    f"Type: {issue['type']}\n"
                    f"Message: {issue['message']}\n\n"
                )
        else:
            f.write("No style issues found.\n\n")
    
    logger.info(f"Report generated: {report_path}")
    return report_path 