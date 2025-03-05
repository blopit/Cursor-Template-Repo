---
description: Multi-agent system workflow for complex tasks
globs: *
---
# Multi-Agent System Workflow

## Roles

### Planner
- **Responsibilities**:
  - High-level analysis
  - Task breakdown
  - Success criteria definition
  - Progress evaluation
- **Tools**:
  - OpenAI o1 model via `tools/plan_exec_llm.py`
  - File analysis with `--file` option
- **Actions**:
  - Invoke planning: `venv/bin/python tools/plan_exec_llm.py --prompt {prompt}`
  - With file context: `venv/bin/python tools/plan_exec_llm.py --prompt {prompt} --file {path}`

### Executor
- **Responsibilities**:
  - Task execution
  - Code implementation
  - Testing
  - Progress reporting
- **Tools**:
  - Standard Cursor tools
  - Development environment
- **Actions**:
  - Update progress tracking
  - Report blockers
  - Request assistance when needed

## Workflow Structure

### Document Sections
1. Background and Motivation
   - User/business requirements
   - Macro objectives
   - Problem context

2. Key Challenges and Analysis
   - Technical barriers
   - Resource constraints
   - Potential risks

3. Verifiable Success Criteria
   - Measurable goals
   - Verification methods

4. High-level Task Breakdown
   - Phase-wise subtasks
   - Module organization

5. Current Status / Progress Tracking
   - Completion status
   - Blockers
   - In-progress items

6. Next Steps and Action Items
   - Specific tasks
   - Assignments
   - Dependencies

7. Executor's Feedback
   - Questions
   - Blockers
   - Information requests

## Guidelines

### Communication
- Declare current role when unclear
- Document all external tool usage
- Keep historical records
- Use appropriate sections for updates

### Task Management
- Planner confirms task completion
- Executor requests confirmation
- Maximum 3 attempts for fixes
- Document lessons learned

### Documentation
- Preserve existing records
- Mark outdated content
- Append new information
- Track reusable solutions 
