# Cursor Rules Documentation

This directory contains rules, templates, and tools for managing Cursor AI rules in your project.

## Directory Structure

```
.cursor/
├── docs/                  # Documentation
│   └── mdc-best-practices.md  # Best practices for creating .mdc files
├── rules/                 # Rule files organized by category
│   ├── core/              # Core rules
│   ├── patterns/          # Pattern rules
│   ├── tech/              # Technology-specific rules
│   └── workflows/         # Workflow rules
├── templates/             # Templates for creating new rules
│   └── rule-template.mdc  # Template for new .mdc files
└── tools/                 # Tools for managing rules
    └── create-mdc-rule.sh # Script to create new rule files
```

## Getting Started

### Creating a New Rule

To create a new rule file based on the template, use the `create-mdc-rule.sh` script:

```bash
.cursor/tools/create-mdc-rule.sh -c <category> -g "<glob-pattern>" <rule-name>
```

For example:

```bash
.cursor/tools/create-mdc-rule.sh -c workflows -g "**/*.js,**/*.ts" tdd-workflow
```

This will:
1. Create a new file at `.cursor/rules/workflows/tdd-workflow.mdc`
2. Prompt you for a description
3. Set up the basic structure based on the template
4. Suggest an entry to add to your `.cursorrules` file

### Adding Rules to .cursorrules

After creating a new rule, add it to the `<available_instructions>` section in your `.cursorrules` file:

```
<available_instructions>
tdd-workflow: Description of your TDD workflow rule
</available_instructions>
```

### Using Rules in Cursor

To use a rule in your Cursor AI conversations, reference it by name:

```
/rule tdd-workflow
```

## Best Practices

For detailed guidelines on creating effective `.mdc` files, see the [Best Practices Guide](docs/mdc-best-practices.md).

Key points:
- Use clear, descriptive names for rule files
- Organize rules into logical categories
- Include proper metadata with glob patterns
- Provide examples and explanations
- Keep rules focused and specific

## Customizing Templates

You can customize the rule template at `.cursor/templates/rule-template.mdc` to better suit your project's needs. Consider creating multiple templates for different types of rules.

## Maintenance

Regularly review and update your rules to ensure they remain relevant and effective. Consider establishing a process for collecting feedback and incorporating improvements. 