---
description: When writing or running tests
globs: *test*.py,*_test.py,test_*.py
---
# Testing Workflow Rules

## Test Categories

### Unit Tests
- Component isolation
- Input/output validation
- Error handling
- Edge cases

### Integration Tests
- Component interaction
- API endpoints
- Database operations
- Authentication flows

### UI Tests
- Component rendering
- User interactions
- State management
- Visual regression

### End-to-End Tests
- User workflows
- System integration
- Performance metrics
- Error scenarios

## Testing Guidelines

### Framework Selection
- Jest for frontend
- Pytest for backend
- Playwright for E2E
- Screenshot utils for visual

### Test Organization
- Clear test descriptions
- Proper setup/teardown
- Meaningful assertions
- Comprehensive coverage

<rule>
name: testing_workflow
description: Rules for testing procedures and quality assurance
filters:
  - type: event
    pattern: "test_run|test_create"
  - type: content
    pattern: "test|spec|describe|it"

actions:
  - type: enforce
    conditions:
      - pattern: "describe.*it"
        message: "Use proper test structure"
      - pattern: "expect.*to"
        message: "Include meaningful assertions"

  - type: suggest
    message: |
      When writing tests:
      1. Use clear descriptions
      2. Test edge cases
      3. Mock external services
      4. Clean up resources
      5. Maintain test data

metadata:
  priority: high
  version: 1.0
</rule> 
