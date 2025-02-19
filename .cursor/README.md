# .cursor Directory Structure

This directory contains all AI assistant-related files and configurations.

## Directory Structure

```
.cursor/
├── rules/              # Core rules and configurations
├── temp/              # Temporary files used during operations
├── cache/             # Cache for API responses and analysis results
├── logs/              # AI operation logs and debugging information
├── snippets/          # Reusable code snippets and templates
├── metrics/           # Performance and usage metrics
├── sessions/          # Session-specific data and context
└── workspace/         # AI workspace for file operations
```

## Directories

### rules/
- Core rules and configurations for the AI assistant
- Stage-specific agent configurations
- Workflow templates and standards

### temp/
- Temporary files used during operations
- Commit message drafts
- Intermediate processing files
- Cleaned up automatically after use

### cache/
- API response caches
- Analysis result caches
- Token usage tracking
- Semantic search indices

### logs/
- Operation logs
- Error tracking
- Performance metrics
- Debug information

### snippets/
- Reusable code templates
- Common refactoring patterns
- Documentation templates
- Test templates

### metrics/
- Usage statistics
- Performance measurements
- Token consumption tracking
- Success/failure rates

### sessions/
- Active session contexts
- Conversation history
- Task progress tracking
- State management

### workspace/
- Temporary working directory for file operations
- Backup copies of modified files
- Generated code pending review
- Test environments 