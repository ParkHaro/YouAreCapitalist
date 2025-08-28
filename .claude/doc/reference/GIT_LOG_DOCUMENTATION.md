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
├── 2025-F0101-T0107-W01.md  # Week 1 of 2025 (Jan 01-07)
├── 2025-F0108-T0114-W02.md  # Week 2 of 2025 (Jan 08-14)
└── timestamps.json          # Last update timestamps
```

### File Naming Convention
**Format**: `YYYY-FMMDD-TMMDD-WNN.md`

- **YYYY**: Year (4 digits)
- **FMMDD**: From Month Day (F + 4 digits)
- **TMMDD**: To Month Day (T + 4 digits)  
- **WNN**: Week Number (W + 2 digits, ISO 8601)

**Examples**:
- `2025-F0826-T0901-W35.md` - Week 35: Aug 26 to Sep 01, 2025
- `2025-F1230-T0105-W01.md` - Week 1: Dec 30 to Jan 05 (year boundary)

### Log File Format
```markdown
# Git Log - [YYYY] Week [N] (F[MMDD]-T[MMDD])
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
3. Create/update weekly log files with `YYYY-FMMDD-TMMDD-WNN.md` format
4. Update timestamp in each modified file
5. Maintain `timestamps.json` with format metadata

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
- File names include both date range and week number for clarity
- Timestamps are updated after each operation
- Existing files are extended, not overwritten
- The system maintains continuity across sessions
- Date format follows MMDD pattern (e.g., 0826 for August 26)

### Timestamp File Structure
```json
{
  "lastUpdate": "2025-08-29T00:00:00Z",
  "lastProcessedWeek": "W35",
  "lastProcessedFile": "2025-F0826-T0901-W35.md",
  "fileFormat": "YYYY-FMMDD-TMMDD-WNN"
}
```