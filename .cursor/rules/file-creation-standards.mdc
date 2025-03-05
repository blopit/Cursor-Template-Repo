---
description: Standards and requirements for creating new files in the project
globs: *.*
---
# File Creation Standards

## Overview
This document outlines the standards and requirements for creating new files in the project. Following these guidelines ensures consistency, proper documentation, and maintainability across the codebase.

## Core Requirements

### 1. File Format Standards

#### General Format Requirements
- Use UTF-8 encoding for all text files
- Use LF (Line Feed) for line endings, not CRLF
- End files with a newline character
- Remove trailing whitespace from all lines
- Use consistent indentation (2 spaces for JavaScript/TypeScript, 4 spaces for Python)

#### Language-Specific Format Requirements

**JavaScript/TypeScript**
- Follow ESLint and Prettier configurations
- Use ES6+ syntax and features
- Include JSDoc comments for functions and classes
- Export only what is necessary
- Include type definitions for TypeScript files

**Python**
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Include docstrings for modules, classes, and functions
- Use snake_case for variables and functions, PascalCase for classes

**CSS/SCSS**
- Use BEM (Block Element Modifier) naming convention
- Group related properties together
- Include comments for complex selectors or rules
- Prefer variables for colors, spacing, and other repeated values

**Markdown**
- Use ATX-style headers (# Header)
- Include a table of contents for longer documents
- Use reference-style links for better readability
- Include alt text for images

### 2. MDC Documentation Requirement
For every new file created in the project, a corresponding MDC (Markdown Cursor) documentation file must be created with the following guidelines:

1. **Location**: MDC files should be placed in the appropriate directory under `.cursor/rules/` based on the file type or functionality.
2. **Naming Convention**: Use kebab-case for MDC filenames (e.g., `component-name.mdc`, `utility-function.mdc`).
3. **Content Structure**: Each MDC file must include:
   - File purpose and overview
   - Usage examples
   - Dependencies and relationships
   - Maintenance considerations

## MDC File Template

```markdown
# [File Name] Documentation

## Purpose
Brief description of what this file does and why it exists.

## Usage
Examples of how to use the functionality provided by this file.

## Dependencies
List of dependencies and relationships with other files/components.

## Maintenance
Guidelines for maintaining and updating this file.

## Additional Notes
Any other relevant information.
```

## File Templates

### JavaScript/TypeScript Component Template
```javascript
/**
 * @fileoverview [Component Name] - [Brief description]
 * @author [Author Name]
 * @created [Creation Date]
 * 
 * Documentation: .cursor/rules/components/[component-name].mdc
 */

import React from 'react';

/**
 * [Component Name] - [Detailed description]
 * 
 * @param {Object} props - Component props
 * @returns {JSX.Element} Rendered component
 */
const ComponentName = (props) => {
  // Implementation
  return (
    <div>
      {/* Component content */}
    </div>
  );
};

export default ComponentName;
```

### Python Module Template
```python
"""
[Module Name] - [Brief description]

This module provides functionality for [purpose].

Documentation: .cursor/rules/python/[module-name].mdc
"""

# Standard library imports
import os
import sys

# Third-party imports
import numpy as np

# Local imports
from .utils import helper_function


class ClassName:
    """
    [Class description]
    
    Attributes:
        attr1 (type): Description of attr1
        attr2 (type): Description of attr2
    """
    
    def __init__(self, param1, param2=None):
        """
        Initialize the class.
        
        Args:
            param1 (type): Description of param1
            param2 (type, optional): Description of param2. Defaults to None.
        """
        self.attr1 = param1
        self.attr2 = param2
    
    def method_name(self, param):
        """
        [Method description]
        
        Args:
            param (type): Description of param
            
        Returns:
            type: Description of return value
        """
        # Implementation
        pass


def function_name(param1, param2=None):
    """
    [Function description]
    
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
```

## Implementation Process

1. **Create the Source File**: Implement the required functionality in the new file using the appropriate template.
2. **Create the MDC File**: Create a corresponding MDC file using the template above.
3. **Cross-Reference**: Ensure the source file includes a comment referencing the MDC file.
4. **Review**: Both files should be reviewed together during code reviews.

## Example

When creating a new component `UserProfile.tsx`:

1. Create the component file with implementation using the JavaScript/TypeScript Component Template
2. Create `.cursor/rules/components/user-profile.mdc` with documentation
3. Ensure the comment in `UserProfile.tsx` references the MDC file: `// Documentation: .cursor/rules/components/user-profile.mdc`

## Exceptions

The following file types are exempt from requiring MDC documentation:
- Test files (ending with `.test.js`, `.spec.js`, etc.)
- Configuration files that follow standard formats (e.g., `.eslintrc`, `.prettierrc`)
- Generated files (marked with a `// GENERATED FILE` comment)

## Enforcement

This rule is enforced through:
- Code review processes
- Pre-commit hooks (when implemented)
- Regular documentation audits
- IDE extensions and linters 
