#!/usr/bin/env python3
"""
File Creator Utility - Creates new files with proper formatting and MDC documentation

This script helps developers create new files following the project's file creation standards,
automatically generating both the source file and its corresponding MDC documentation.

Documentation: .cursor/rules/tools/create-file.mdc
"""

import os
import sys
import argparse
import datetime
from pathlib import Path
import getpass

# Templates for different file types
TEMPLATES = {
    "js": {
        "extension": ".js",
        "template": '''/**
 * @fileoverview {name} - {description}
 * @author {author}
 * @created {date}
 * 
 * Documentation: {mdc_path}
 */

/**
 * {description}
 */

// Implementation
''',
        "mdc_dir": "javascript"
    },
    "jsx": {
        "extension": ".jsx",
        "template": '''/**
 * @fileoverview {name} - {description}
 * @author {author}
 * @created {date}
 * 
 * Documentation: {mdc_path}
 */

import React from 'react';

/**
 * {name} - {description}
 * 
 * @param {{}} props - Component props
 * @returns {{JSX.Element}} Rendered component
 */
const {name} = (props) => {{
  // Implementation
  return (
    <div>
      {{/* Component content */}}
    </div>
  );
}};

export default {name};
''',
        "mdc_dir": "components"
    },
    "ts": {
        "extension": ".ts",
        "template": '''/**
 * @fileoverview {name} - {description}
 * @author {author}
 * @created {date}
 * 
 * Documentation: {mdc_path}
 */

/**
 * {description}
 */

// Implementation
''',
        "mdc_dir": "typescript"
    },
    "tsx": {
        "extension": ".tsx",
        "template": '''/**
 * @fileoverview {name} - {description}
 * @author {author}
 * @created {date}
 * 
 * Documentation: {mdc_path}
 */

import React from 'react';

interface {name}Props {{
  // Define props here
}}

/**
 * {name} - {description}
 * 
 * @param {{{name}Props}} props - Component props
 * @returns {{JSX.Element}} Rendered component
 */
const {name}: React.FC<{name}Props> = (props) => {{
  // Implementation
  return (
    <div>
      {{/* Component content */}}
    </div>
  );
}};

export default {name};
''',
        "mdc_dir": "components"
    },
    "py": {
        "extension": ".py",
        "template": '''"""
{name} - {description}

This module provides functionality for {description}.

Documentation: {mdc_path}
"""

# Standard library imports

# Third-party imports

# Local imports


class {name}:
    """
    {description}
    
    Attributes:
        attr1 (type): Description of attr1
    """
    
    def __init__(self, param1, param2=None):
        """
        Initialize the class.
        
        Args:
            param1 (type): Description of param1
            param2 (type, optional): Description of param2. Defaults to None.
        """
        self.attr1 = param1
    
    def method_name(self, param):
        """
        Method description
        
        Args:
            param (type): Description of param
            
        Returns:
            type: Description of return value
        """
        # Implementation
        pass


def function_name(param1, param2=None):
    """
    Function description
    
    Args:
        param1 (type): Description of param1
        param2 (type, optional): Description of param2. Defaults to None.
        
    Returns:
        type: Description of return value
    """
    # Implementation
    pass


if __name__ == "__main__":
    # Code to execute when run as a script
    pass
''',
        "mdc_dir": "python"
    },
    "css": {
        "extension": ".css",
        "template": '''/**
 * {name} - {description}
 * @author {author}
 * @created {date}
 * 
 * Documentation: {mdc_path}
 */

/* Variables */
:root {{
  /* Colors */
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  
  /* Spacing */
  --spacing-small: 8px;
  --spacing-medium: 16px;
  --spacing-large: 24px;
}}

/* Main styles */
.{name_kebab} {{
  /* Add styles here */
}}
''',
        "mdc_dir": "styles"
    },
    "scss": {
        "extension": ".scss",
        "template": '''/**
 * {name} - {description}
 * @author {author}
 * @created {date}
 * 
 * Documentation: {mdc_path}
 */

// Variables
$primary-color: #007bff;
$secondary-color: #6c757d;

// Spacing
$spacing-small: 8px;
$spacing-medium: 16px;
$spacing-large: 24px;

// Main styles
.{name_kebab} {{
  // Add styles here
  
  &__element {{
    // Element styles
  }}
  
  &--modifier {{
    // Modifier styles
  }}
}}
''',
        "mdc_dir": "styles"
    },
    "md": {
        "extension": ".md",
        "template": '''# {name}

## Overview

{description}

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

Installation instructions here.

## Usage

Usage instructions here.

## API

API documentation here.

## Examples

Examples here.

## Contributing

Contribution guidelines here.

## License

License information here.
''',
        "mdc_dir": "markdown"
    }
}

# MDC documentation template
MDC_TEMPLATE = '''---
description: {description}
globs: {glob_pattern}
---
# {name} Documentation

## Purpose
{description}

## Usage
Examples of how to use the functionality provided by this file.

```{code_block_type}
// Usage example code here
```

## Dependencies
List of dependencies and relationships with other files/components:

- List dependencies here
- Include both internal and external dependencies

## Maintenance
Guidelines for maintaining and updating this file:

- Document update procedures
- Note testing requirements
- List related files to update

## Additional Notes
Any other relevant information about this file.
'''


def to_kebab_case(name):
    """Convert a name to kebab-case."""
    return name.replace(' ', '-').lower()


def to_pascal_case(name):
    """Convert a name to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def create_file(file_path, file_type, name, description, author):
    """Create a new file with the appropriate template."""
    if file_type not in TEMPLATES:
        print(f"Error: Unsupported file type '{file_type}'")
        sys.exit(1)
    
    # Get template info
    template_info = TEMPLATES[file_type]
    
    # Ensure the file has the correct extension
    if not file_path.endswith(template_info["extension"]):
        file_path += template_info["extension"]
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
    
    # Generate MDC path
    mdc_dir = f".cursor/rules/{template_info['mdc_dir']}"
    os.makedirs(mdc_dir, exist_ok=True)
    
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    mdc_file_name = to_kebab_case(base_name) + ".mdc"
    mdc_path = f"{mdc_dir}/{mdc_file_name}"
    
    # Format the template
    pascal_name = to_pascal_case(base_name)
    kebab_name = to_kebab_case(base_name)
    
    content = template_info["template"].format(
        name=pascal_name,
        name_kebab=kebab_name,
        description=description,
        author=author,
        date=datetime.datetime.now().strftime("%Y-%m-%d"),
        mdc_path=mdc_path
    )
    
    # Write the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created file: {file_path}")
    
    # Generate appropriate glob pattern based on file type and path
    glob_pattern = os.path.join(os.path.dirname(file_path), f"*.{file_type}")
    
    # Create MDC documentation
    code_block_type = file_type
    if file_type in ["jsx", "tsx"]:
        code_block_type = "jsx"
    
    mdc_content = MDC_TEMPLATE.format(
        name=pascal_name,
        description=description,
        code_block_type=code_block_type,
        glob_pattern=glob_pattern
    )
    
    with open(mdc_path, 'w', encoding='utf-8') as f:
        f.write(mdc_content)
    
    print(f"Created MDC documentation: {mdc_path}")


def main():
    """Main function to parse arguments and create files."""
    parser = argparse.ArgumentParser(description="Create a new file with proper formatting and MDC documentation")
    parser.add_argument("file_path", help="Path to the new file")
    parser.add_argument("--type", "-t", required=True, choices=TEMPLATES.keys(), 
                        help="Type of file to create")
    parser.add_argument("--description", "-d", default="", 
                        help="Brief description of the file")
    parser.add_argument("--author", "-a", default=getpass.getuser(),
                        help="Author of the file (defaults to current user)")
    
    args = parser.parse_args()
    
    # Extract name from file path
    file_name = os.path.basename(args.file_path)
    base_name = os.path.splitext(file_name)[0]
    
    create_file(args.file_path, args.type, base_name, args.description, args.author)


if __name__ == "__main__":
    main() 
