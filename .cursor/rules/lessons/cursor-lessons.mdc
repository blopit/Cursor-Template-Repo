---
description: Lessons learned from using Cursor
globs: *
---
# Cursor-Specific Lessons

## Environment Setup
- Python virtual environment is located in `./venv`
- Use the venv for all Python-related operations

## Debugging and Logging
- Include information useful for debugging in program output
- Add debug information to stderr while keeping main output clean in stdout for better pipeline integration

## Code Editing Best Practices
- Always read file contents before attempting to edit
- When using seaborn styles in matplotlib, use 'seaborn-v0_8' instead of 'seaborn' due to recent version changes

## Git and GitHub Operations
- For multiline commit messages:
  1. Write the message in a temporary file
  2. Use `git commit -F <filename>` to commit
  3. Remove the temporary file afterward
  4. Include "[Cursor] " prefix in commit messages and PR titles

## Search and Encoding
- Ensure proper handling of different character encodings (UTF-8) for international queries

## LLM Model Usage
- OpenAI:
  - Use `gpt-4o` as the default model (latest with vision capabilities)
  - Use `o1` for advanced tasks (reasoning, planning, or when blocked)
- Claude:
  - Use `claude-3-5-sonnet-20241022` as the latest model with vision capabilities 
