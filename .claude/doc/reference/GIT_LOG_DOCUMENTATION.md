---
category: reference
tags: [git, documentation, automation, logging]
related: [DOCUMENTATION_GUIDELINES.md]
parent: INDEX.md
created: 2025-08-28
updated: 2025-08-28
priority: medium
---

# Git Log Documentation System

[🇰🇷 한국어 버전](./GIT_LOG_DOCUMENTATION_KOR.md)

## 📍 Navigation

[↩️ Back to Reference](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## document_log_git Command

Automatically analyze and document git history in weekly segments.

### Syntax
```bash
document_log_git [period]
```

### Parameters
- **`period`** (optional): Time period to analyze
  - Format: `YYYY-MM-DD` to `YYYY-MM-DD`
  - Example: `2024-01-01 to 2024-01-31`
  - If omitted: Uses last timestamp from existing logs to current date

### Output Structure
```
claude_root/project_log/
├── 2024-W01.md  # Week 1 of 2024
├── 2024-W02.md  # Week 2 of 2024
└── timestamps.json  # Last update timestamps
```

### Log File Format
```markdown
# Git Log - Week [N] of [YYYY]
**Period**: [Start Date] - [End Date]
**Last Updated**: [Timestamp]

## Summary
- Total commits: [N]
- Contributors: [List]
- Main areas: [List]

## Daily Breakdown
### [Date]
- [Commit Hash] - [Author] - [Message]
- [Analysis of changes]

## Key Changes
- [Significant features/fixes]
```

### Workflow
1. Parse git log for specified period (or from last timestamp)
2. Group commits by ISO week (Monday-Sunday)
3. Create/update weekly log files in `claude_project_log/`
4. Update timestamp in each modified file
5. Maintain `timestamps.json` for tracking

### Examples
```bash
# Analyze specific period
document_log_git "2024-01-01 to 2024-01-31"

# Continue from last timestamp
document_log_git

# Analyze last month
document_log_git "last month"

# Analyze since specific date
document_log_git "since 2024-01-15"
```

### Implementation Notes
- Logs are organized by ISO week numbers
- Each week runs Monday to Sunday
- Timestamps are updated after each operation
- Existing files are extended, not overwritten
- The system maintains continuity across sessions