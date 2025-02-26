# Cursor Rules Tools

This directory contains tools to help manage and use Cursor rules effectively.

## Template Selector Script

The `template-selector.sh` script helps you select and copy templates from the `awesome-cursor-rules-mdc` directory to the appropriate location in your project's `.cursor/rules` directory.

### Usage

```bash
# Make sure the script is executable
chmod +x .cursor/rules/tools/template-selector.sh

# Run the script
.cursor/rules/tools/template-selector.sh
```

### Features

- Interactive selection of templates by category
- Automatic copying of templates to the appropriate directory
- Color-coded output for better readability
- Confirmation before copying files
- Helpful reminders to update glob patterns

### Categories

The script organizes templates into the following categories:

1. **Frontend Frameworks**: React, Next.js, Vue.js, Svelte/SvelteKit, Solid.js, Qwik
2. **Backend Frameworks**: Python (FastAPI/Django), Node.js/Express, NestJS, Laravel/PHP
3. **Full Stack Solutions**: Next.js + TypeScript, TypeScript + React + Supabase, MERN Stack, TypeScript + shadcn/ui + Next.js
4. **Mobile Development**: React Native, React Native + Expo, SwiftUI
5. **Data Science & ML**: Python LLM and ML workflow, PyTorch and scikit-learn, Pandas and scikit-learn
6. **Blockchain**: Solidity with Hardhat, Solidity with React
7. **Other**: TypeScript Configuration, Tailwind CSS Setup, Testing Frameworks

### After Copying Templates

After copying a template, remember to:

1. Review the template files to ensure they match your project's requirements
2. Update glob patterns in the template files to match your project structure
3. Customize the rules as needed for your specific use case

## Other Tools

Additional tools may be added to this directory in the future to help with:

- Validating rule files
- Generating new rule files from existing code
- Analyzing rule usage and effectiveness
- Automating rule updates

Check back regularly for updates and new tools. 