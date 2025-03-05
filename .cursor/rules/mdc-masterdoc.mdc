---
description: Master documentation for MDC file creation and management standards
globs: ".cursor/rules/**/*.mdc"
---

# MDC (Markdown Cursor) Master Documentation

## Overview
MDC files are specialized Markdown files containing Cursor-specific rules, documentation, and glob patterns for AI assistance. Every file in the `src` directory must have a corresponding `.mdc` file in `.cursor/rules/src` with matching directory structure. This hierarchical organization ensures that rules are applied contextually to the specific files they govern.

## Directory Structure

### Root Structure
- `.cursor/rules/src/`: Mirror of src/ directory structure containing rules for each source file and directory
- `.cursor/rules/tools/`: Documentation for project tools
- `.cursor/rules/workflows/`: Workflow-specific guidelines
- `.cursor/rules/core/`: Core system rules
- `.cursor/rules/awesome-cursor-rules-mdc/`: Specialized rule templates

### Source Code Rules Hierarchy
The `.cursor/rules/src/` directory maintains an exact mirror of the source code's directory structure. For example:
```
src/
  components/
    Button.tsx
    Card.tsx
  utils/
    formatting.ts
    validation.ts

.cursor/rules/src/
  components/
    Button.mdc  # Rules specific to Button.tsx
    Card.mdc    # Rules specific to Card.tsx
  utils/
    formatting.mdc  # Rules specific to formatting.ts
    validation.mdc  # Rules specific to validation.ts
```

This hierarchical organization provides several benefits:
- Contextual rule application based on file location
- Easy navigation between source files and their corresponding rules
- Inheritance of rules from parent directories to child files
- Clear organization that scales with project complexity

### File Organization
- Mirror src/ directory structure exactly, maintaining the same hierarchy
- Use appropriate subdirectories based on file type and component relationships
- Follow consistent naming conventions that match source files
- Maintain clear separation of concerns with directory-specific rules
- Allow for inheritance of rules from parent directories to child files

## File Naming Standards

### Conventions
- Use kebab-case for all MDC filenames (e.g., `component-name.mdc`)
- Names should be descriptive and reflect content/purpose
- For glob-specific files, include "glob" in filename
- File extension must be `.mdc`

### Hierarchical Naming
- Source file rules should match their source file names (e.g., `Button.tsx` → `Button.mdc`)
- Directory rules should use `_index.mdc` or `directory-name.mdc` to apply rules to all files in that directory
- Parent directory rules cascade down to subdirectories unless explicitly overridden
- More specific rules (file-level) take precedence over more general rules (directory-level)

### Naming Patterns
- Individual file rules: `filename.mdc`
- Directory-level rules: `_index.mdc` or `directory-name.mdc`
- Feature-specific rules: `feature-name.mdc`
- Global type rules: `type-glob.mdc` (e.g., `typescript-glob.mdc`, `scss-glob.mdc`)

## Required File Format

### Metadata Header
```markdown
---
description: Brief description of the file's purpose
globs: Pattern matching files this MDC applies to
---
```

### Core Sections
1. Title: Clear, descriptive title
2. Purpose: What this file does/why it exists
3. Usage Guidelines: How to use the code
4. Dependencies: Related files/modules
5. Best Practices: Specific guidelines
6. Examples: Usage examples if applicable

## Creation Methods

### 1. Automatic Creation
```bash
# For single file
node tools/create_mdc_file.js src/path/to/file.js

# For all files
node tools/create_all_mdc_files.js
```

### 2. Manual Creation
Use `tools/create_file.py` to create both source and MDC files:
```bash
python tools/create_file.py path/to/file --type filetype --description "Description"
```

### 3. Pre-commit Hook
- Automatically creates MDC files for new files
- Enforces MDC documentation requirements
- Blocks commits without proper MDC documentation

## Content Requirements

### Technical Standards
- UTF-8 encoding required
- LF line endings (not CRLF)
- End files with newline
- Remove trailing whitespace
- 2-space indentation
- 100 character line length maximum

### Documentation Standards
- Clear, concise language
- Practical examples
- Complete all required sections
- Cross-reference related files
- Keep documentation current

## Enforcement

### Automated Enforcement
- Pre-commit hooks
- Creation scripts
- Validation tools
- IDE extensions
- Regular audits

### Manual Verification
- Code review process
- Documentation reviews
- Regular maintenance
- Update checks

## Exceptions

The following don't require MDC documentation:
- Test files (*.test.js, *.spec.js)
- Standard configuration files (.eslintrc, etc.)
- Generated files (marked with "GENERATED FILE" comment)

## Maintenance

### Regular Tasks
- Review and update MDC files as code changes
- Verify documentation accuracy
- Update examples as needed
- Check for broken references
- Clean up obsolete files

### Safety Rules
- Create backups before bulk changes
- Verify system functionality after updates
- Test documentation accuracy
- Maintain version history
- Document significant changes

## Versioning and Change Management

### Version Control
- MDC files should be committed to version control alongside source code
- Include MDC file changes in the same commits as related source code changes
- Document significant MDC rule changes in commit messages
- Use pull requests to review MDC rule changes

### Change Management
- Document the rationale for rule changes
- Notify team members of significant rule changes
- Consider the impact of rule changes on existing code
- Implement changes gradually for major rule modifications

### Backward Compatibility
- Maintain backward compatibility when possible
- Document breaking changes clearly
- Provide migration paths for significant rule changes
- Use deprecation notices before removing rules

### Rule Evolution
- Regularly review and update rules based on project needs
- Collect feedback on rule effectiveness
- Adapt rules as the project evolves
- Archive obsolete rules rather than deleting them

## Tools Reference

### Core Tools
- `tools/create_mdc_file.js`: Creates single MDC file
- `tools/create_all_mdc_files.js`: Bulk MDC creation
- `tools/create_file.py`: Creates both source and MDC files
- `tools/hooks/pre-commit`: Enforces MDC requirements

### Installation
```bash
# Install git hooks
./tools/install_hooks.sh
```

## Benefits
1. Consistent Documentation
2. Enforced Standards
3. Clear Guidelines
4. Improved Onboarding
5. Better Maintainability
6. AI-Assisted Development

## YAML Frontmatter Notes

### Description Field
The `description` field is visible to the AI agent, which uses it to decide whether to read the full rule. If no description is provided, only the attach rules below will be used.

### Globs Field
The `globs` field specifies patterns (e.g., `*.py` or `client/**/*.tsx`) that determine which files this rule will automatically be included for in AI responses. When a file matching these patterns is being worked on, this rule will be automatically attached to the conversation. 

## Special Considerations for MDC Glob Files

### Glob Pattern Specificity
- Make glob patterns as specific as possible to avoid unintended matches
- Document the rationale behind each glob pattern
- Test glob patterns against the codebase to ensure they match the intended files

### Rule Inheritance and Precedence
- Rules follow a hierarchical inheritance model from parent directories to child files
- More specific rules (file-level) override more general rules (directory-level)
- The precedence order from highest to lowest is:
  1. File-specific rules (e.g., `Button.mdc` for `Button.tsx`)
  2. Immediate directory rules (e.g., `components/_index.mdc`)
  3. Parent directory rules (e.g., `src/_index.mdc`)
  4. Global type-specific rules (e.g., `typescript-glob.mdc`)
  5. Project-wide rules (e.g., `general-software.mdc`)
- When multiple MDC glob files match the same file, document the precedence order
- Use explicit overrides when necessary by noting which rules take precedence

### Rule Conflicts
- When multiple MDC glob files match the same file, document the precedence order
- Avoid conflicting rules across different MDC glob files
- Use cross-references to indicate relationships between related MDC glob files 

## Tools and Automation for MDC Files

### MDC Validation Tools
- Use validation tools to ensure MDC files follow the correct format
- Validate YAML frontmatter syntax and required fields
- Check for proper glob pattern formatting (quoted strings)
- Verify that referenced files and directories exist

### Automation Scripts
- Create scripts to generate MDC files from templates
- Automate the creation of MDC files for new source files
- Use scripts to validate MDC files during CI/CD processes
- Implement tools to check for missing MDC files

### Integration with Development Workflow
- Include MDC file creation in project setup scripts
- Add MDC validation to pre-commit hooks
- Document MDC requirements in onboarding materials
- Provide templates for common MDC file types

### MDC Maintenance Tools
- Create tools to detect orphaned MDC files (no matching source files)
- Implement scripts to update glob patterns when file structures change
- Use tools to analyze rule coverage across the codebase
- Develop utilities to visualize rule inheritance and conflicts 