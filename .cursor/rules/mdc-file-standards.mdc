---
description: Standards and requirements for creating and maintaining Markdown Cursor (.mdc) files
globs: ".cursor/rules/**/*.mdc"
---

# MDC File Standards

## Overview
This document outlines the standards and requirements for creating and maintaining Markdown Cursor (`.mdc`) files in the project. MDC files are specialized Markdown files that contain Cursor-specific rules, documentation, and glob patterns for AI assistance. Following these guidelines ensures consistency, proper organization, and effective AI assistance across the codebase.

## Core Requirements

### 1. MDC File Format Standards

#### General Format Requirements
- Use UTF-8 encoding for all MDC files
- Use LF (Line Feed) for line endings, not CRLF
- End files with a newline character
- Remove trailing whitespace from all lines
- Use consistent indentation (2 spaces for all MDC files)
- Maximum line length of 100 characters for better readability

#### MDC-Specific Format Requirements
- Use ATX-style headers (# Header)
- Include a table of contents for longer documents
- Use reference-style links for better readability
- Include alt text for images
- Use code blocks with language specifiers for code examples
- Use bullet points for lists rather than numbered lists unless sequence is important
- Use blockquotes for important notes or warnings

### 2. MDC File Organization

#### Directory Structure
MDC files should be organized in the following directory structure under `.cursor/rules/`:

```
.cursor/
  rules/
    core/                 # Fundamental rules and system configurations
    workflows/            # Specific workflow guidelines and procedures
    tools/                # Tool-specific rules and usage guidelines
    lessons/              # Accumulated knowledge and learned best practices
    components/           # UI component documentation
    api/                  # API endpoint documentation
    database/             # Database schema and query documentation
    utilities/            # Utility function documentation
    awesome-cursor-rules-mdc/  # Collection of specialized rule templates
```

#### Naming Convention
- Use kebab-case for MDC filenames (e.g., `component-name.mdc`, `utility-function.mdc`)
- Names should be descriptive and reflect the content or purpose
- For glob-specific MDC files, include the word "glob" in the filename (e.g., `typescript-glob.mdc`, `react-component-glob.mdc`)

### 3. MDC Content Structure

Every MDC file must include the following sections:

#### Required Sections
1. **Title**: Clear, descriptive title at the top of the file
2. **Purpose**: Brief description of what this MDC file defines and why it exists
3. **Glob Patterns**: List of glob patterns that this MDC file applies to (for glob-specific files)
4. **Rules**: The actual rules, guidelines, or documentation content
5. **Examples**: Practical examples demonstrating the application of the rules
6. **Related MDC Files**: References to other related MDC files

#### Optional Sections
1. **Exceptions**: Cases where the rules don't apply
2. **Enforcement**: How the rules are enforced
3. **Version History**: Changes made to the MDC file over time
4. **Additional Notes**: Any other relevant information

## MDC Glob File Template

```markdown
# [Title] Glob Rules

## Purpose
Brief description of what these glob rules define and why they exist.

## Glob Patterns
- `**/*.ts`
- `**/*.tsx`
- `src/**/*.js`
- (Add other relevant glob patterns)

## Rules
Detailed description of the rules that apply to files matching these glob patterns.

### Rule Category 1
- Rule 1
- Rule 2
- Rule 3

### Rule Category 2
- Rule 1
- Rule 2
- Rule 3

## Examples
Examples demonstrating the application of these rules.

### Example 1
```[language]
// Example code or content
```

### Example 2
```[language]
// Example code or content
```

## Related MDC Files
- [related-mdc-file-1.mdc](mdc:../path/to/related-mdc-file-1.mdc)
- [related-mdc-file-2.mdc](mdc:../path/to/related-mdc-file-2.mdc)

## Exceptions
Cases where these rules don't apply.

## Enforcement
How these rules are enforced.

## Version History
- 2023-10-01: Initial version
- 2023-11-15: Added new rule for X
```

## Implementation Process

1. **Identify File Types**: Determine which file types or patterns need specific rules
2. **Create MDC Glob File**: Create a new MDC file using the template above
3. **Define Glob Patterns**: List all glob patterns that the rules apply to
4. **Define Rules**: Document the rules, guidelines, and best practices
5. **Add Examples**: Include practical examples demonstrating the rules
6. **Cross-Reference**: Link to related MDC files for additional context
7. **Review**: Have the MDC file reviewed for accuracy and completeness

## Example Glob-Specific MDC Files

### TypeScript Glob Example

```markdown
# TypeScript Development Rules

## Purpose
This file defines rules and best practices for TypeScript development in the project.

## Glob Patterns
- `**/*.ts`
- `**/*.tsx`
- `src/**/*.ts`
- `src/**/*.tsx`

## Rules
### Type Safety
- Always use explicit types for function parameters and return values
- Avoid using `any` type unless absolutely necessary
- Use interfaces for object shapes
- Use type aliases for complex types

### Code Organization
- Group imports by source (built-in, external, internal)
- Use barrel exports for related functionality
- Keep files focused on a single responsibility

## Examples
### Good Type Usage
```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

function getUserById(id: string): Promise<User | null> {
  // Implementation
}
```

## Related MDC Files
- [react-component-glob.mdc](mdc:../components/react-component-glob.mdc)
- [testing-typescript-glob.mdc](mdc:../testing/testing-typescript-glob.mdc)
```

### React Component Glob Example

```markdown
# React Component Rules

## Purpose
This file defines rules and best practices for React components in the project.

## Glob Patterns
- `**/*.tsx`
- `src/components/**/*.tsx`
- `src/pages/**/*.tsx`

## Rules
### Component Structure
- Use functional components with hooks
- Keep components small and focused
- Extract complex logic into custom hooks
- Use proper prop typing

### Styling
- Use CSS modules for component styling
- Follow BEM naming convention for class names
- Use theme variables for colors and spacing

## Examples
### Good Component Structure
```tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  text: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

const Button: React.FC<ButtonProps> = ({ text, onClick, variant = 'primary' }) => {
  return (
    <button 
      className={`${styles.button} ${styles[`button--${variant}`]}`}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default Button;
```

## Related MDC Files
- [typescript-glob.mdc](mdc:../typescript-glob.mdc)
- [css-modules-glob.mdc](mdc:../styling/css-modules-glob.mdc)
```

## Special Considerations for MDC Glob Files

### Glob Pattern Specificity
- Make glob patterns as specific as possible to avoid unintended matches
- Document the rationale behind each glob pattern
- Test glob patterns against the codebase to ensure they match the intended files

### Rule Conflicts
- When multiple MDC glob files match the same file, document the precedence order
- Avoid conflicting rules across different MDC glob files
- Use cross-references to indicate relationships between related MDC glob files

### Maintenance
- Review and update MDC glob files regularly as the codebase evolves
- Document changes in the Version History section
- Ensure examples remain relevant and up-to-date

## Enforcement

MDC file standards are enforced through:
- Code review processes
- Pre-commit hooks (when implemented)
- Regular documentation audits
- IDE extensions and linters
- Automated validation scripts

## Conclusion

Following these standards for MDC files, especially those containing glob patterns, ensures that AI assistance is consistent, accurate, and helpful across the project. Well-structured MDC files improve developer experience, reduce errors, and maintain code quality throughout the development lifecycle.