# Best Practices for Creating .mdc Files for Cursor

This document serves as a guide for creating high-quality `.mdc` files used by Cursor to enforce coding standards, workflows, and other development practices. Follow these guidelines to ensure your files are consistent, readable, and effective.

## 1. Understand the Purpose of .mdc Files

- **Definition**: `.mdc` files are Markdown documents enriched with metadata and instructions. They are used by Cursor to define rules, guidelines, and workflows for your project.
- **Use Case**: Use these files to enforce test-driven development (TDD), documentation standards, CI/CD pipelines, and other project-specific rules.

*Visualize this as a blueprint document where each rule acts as a building block in your overall development process.*

## 2. File Naming and Organization

- **File Extension**: Ensure your file names end with the `.mdc` extension.
- **Directory Structure**:  
  - Organize files into logical subdirectories (e.g., `workflows/`, `core/`, etc.).
  - Maintain a central configuration file (e.g., `.cursorrules`) that lists all available instructions.
- **Naming Conventions**:
  - Use kebab-case for file names (e.g., `clean-architecture.mdc`).
  - Choose descriptive names that reflect the content and purpose.

*Imagine a well-organized filing cabinet where each folder and file is labeled by its purpose.*

## 3. Metadata Block

At the beginning of each `.mdc` file, include a metadata block enclosed by triple dashes (`---`). This block provides essential information that Cursor uses to apply the rules correctly.

### Key Metadata Fields:

- **description**: A brief summary of the rule's purpose.
- **globs**: File pattern matching rules (e.g., `**/*.{py,js,ts}`) that determine which files the rule applies to.
- **Any Additional Fields**: Depending on your use case, you might include version numbers, authorship, or tags.

### Example Metadata Block:

```yaml
---
description: Enforces TDD practices for Python and JavaScript files
globs: **/*.{py,js}
---
```

## 4. Content Structure

Structure the content of your `.mdc` files in a clear, hierarchical manner:

- **Headings**: Use Markdown headings to organize content (e.g., `# Main Title`, `## Section`, `### Subsection`).
- **Lists**: Use bullet points or numbered lists for guidelines, steps, or examples.
- **Code Blocks**: Include code examples using triple backticks with language specification.
- **Tables**: Use tables to present structured data or comparisons.

### Example Structure:

```markdown
# Rule Title

## Overview
Brief description of the rule's purpose and importance.

## Guidelines
- Guideline 1: Explanation
- Guideline 2: Explanation

## Examples
```python
# Example code demonstrating the rule
def example_function():
    pass
```

## Best Practices
1. First best practice
2. Second best practice
```

## 5. Writing Effective Rules

- **Be Specific**: Clearly define what is expected and what is prohibited.
- **Provide Context**: Explain why the rule exists and what problems it solves.
- **Include Examples**: Demonstrate both correct and incorrect implementations.
- **Use Consistent Terminology**: Maintain consistent terminology throughout your rules.

*Think of each rule as a clear instruction that leaves no room for misinterpretation.*

## 6. Glob Pattern Best Practices

Glob patterns determine which files your rules apply to. Follow these best practices:

- **Be Specific**: Target only the file types that the rule applies to.
- **Use Multiple Patterns**: Separate multiple patterns with commas (e.g., `**/*.js,**/*.ts`).
- **Consider Exclusions**: Use negative patterns to exclude specific files or directories (e.g., `!node_modules/**`).
- **Test Your Patterns**: Verify that your patterns match the intended files.

### Common Glob Patterns:

| Pattern | Description | Example |
|---------|-------------|---------|
| `**/*.{ext1,ext2}` | All files with specified extensions | `**/*.{js,ts}` |
| `path/**/*.ext` | Files with extension in specific directory | `src/**/*.py` |
| `!pattern` | Exclude files matching pattern | `!node_modules/**` |
| `**/prefix*.ext` | Files with specific prefix | `**/test*.js` |

## 7. Integration with Cursor

- **Reference in `.cursorrules`**: Ensure your `.mdc` files are referenced in the central `.cursorrules` file.
- **Categorization**: Group related rules together in the available instructions section.
- **Descriptive Summaries**: Provide clear, concise descriptions for each rule.

### Example `.cursorrules` Entry:

```
<available_instructions>
clean-architecture: Guidelines for implementing clean architecture patterns
tdd-practices: Detailed Test-Driven Development practices
documentation-standards: Documentation requirements for all project artifacts
</available_instructions>
```

## 8. Maintenance and Updates

- **Version Control**: Keep your `.mdc` files under version control.
- **Regular Reviews**: Periodically review and update rules to reflect evolving best practices.
- **Changelog**: Maintain a changelog to track significant changes to rules.
- **Feedback Loop**: Establish a process for collecting and incorporating feedback on rules.

## 9. Common Pitfalls to Avoid

- **Overly Complex Rules**: Keep rules simple and focused on specific concerns.
- **Inconsistent Formatting**: Maintain consistent formatting across all `.mdc` files.
- **Outdated Information**: Regularly review and update rules to reflect current practices.
- **Conflicting Rules**: Ensure rules don't contradict each other.
- **Insufficient Examples**: Always include clear examples to illustrate rules.

## 10. Advanced Techniques

- **Cross-References**: Reference related rules using links or identifiers.
- **Templates**: Create templates for common rule types to ensure consistency.
- **Rule Categories**: Organize rules into categories for easier navigation.
- **Conditional Rules**: Specify conditions under which rules apply.

## Conclusion

Well-crafted `.mdc` files are essential for maintaining consistent development practices across your project. By following these guidelines, you can create clear, effective rules that enhance code quality and streamline development workflows.

Remember that the ultimate goal of these rules is to support developers in writing high-quality code, not to impose unnecessary restrictions. Strike a balance between providing helpful guidance and allowing for flexibility and creativity. 