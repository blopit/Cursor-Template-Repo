---
description: When implementing improvements and optimizations to code, processes, or workflows
globs: *.py,*.ts,*.tsx,*.md,*.log,benchmark_*.json,perf_*.json
---
# Continuous Improvement Rules

## Performance Monitoring

### Benchmarking
- Implement performance benchmarks
- Track response times
- Monitor resource usage
- Log performance metrics
- Compare across versions

### Resource Usage
- Monitor memory consumption
- Track CPU utilization
- Log I/O operations
- Measure network latency
- Analyze database performance

## Code Quality

### Static Analysis
- Run pylint/flake8 regularly
- Maintain consistent code style
- Track code complexity metrics
- Monitor test coverage
- Use type hints and validate with mypy

### Refactoring Triggers
- Methods > 50 lines
- Cyclomatic complexity > 10
- Duplicate code blocks
- Unclear naming
- Missing documentation
- Low test coverage areas

## Documentation

### Living Documentation
- Keep docs current
- Update with changes
- Document API changes
- Maintain changelog
- Update architecture diagrams

### Knowledge Sharing
- Document lessons learned
- Share optimization insights
- Record debugging steps
- Maintain troubleshooting guides
- Document performance improvements

## Metrics Collection

### Key Indicators
- Response times
- Error rates
- Test coverage
- Code quality scores
- Build times
- Deployment frequency
- Time to recovery

### Improvement Tracking
- Set baseline metrics
- Define improvement goals
- Track progress weekly
- Report on outcomes
- Adjust strategies based on data

## Process Automation

### CI/CD Enhancement
- Automate repetitive tasks
- Add pre-commit hooks
- Enhance test automation
- Streamline deployment
- Automate dependency updates

### Tool Development
- Create helper scripts
- Build debugging tools
- Develop monitoring utilities
- Implement automation scripts
- Create development utilities

## Review Process

### Code Reviews
- Check for performance impacts
- Verify error handling
- Ensure proper logging
- Validate documentation
- Review test coverage

### Architecture Reviews
- Monthly architecture reviews
- Scalability assessment
- Security evaluation
- Dependency analysis
- Technical debt review

## Important Principles

### Question Assumptions
- Challenge existing processes
- Verify improvement metrics
- Test alternative approaches
- Get team feedback
- Document findings

### Avoid Over-optimization
- Focus on measurable improvements
- Prioritize critical paths
- Balance effort vs. benefit
- Consider maintenance cost
- Keep solutions simple

<rule>
name: continuous_improvement
description: Rules for maintaining and improving code quality and processes
filters:
  - type: event
    pattern: "improvement|optimization|refactor"
  - type: content
    pattern: "improve|optimize|enhance|refactor"

actions:
  - type: enforce
    conditions:
      - pattern: "performance_change"
        message: "Include benchmark results"
      - pattern: "optimization"
        message: "Document improvement metrics"
      - pattern: "refactor"
        message: "Maintain test coverage"

  - type: suggest
    message: |
      For improvements:
      1. Measure before changing
      2. Document baseline
      3. Test thoroughly
      4. Monitor results
      5. Share knowledge
      6. Question assumptions
      7. Keep it simple
      8. Consider maintenance
      9. Get feedback
      10. Track metrics

metadata:
  priority: high
  version: 1.0
</rule> 
