---
category: guidelines
tags: [documentation, standards, dual-language]
related: []
parent: INDEX.md
created: 2025-08-28
updated: 2025-08-28
priority: high
---

# Documentation Guidelines

[🇰🇷 한국어 버전](./DOCUMENTATION_GUIDELINES_KOR.md)

## 📍 Navigation

[↩️ Back to Guidelines](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## Dual-Language Documentation System

All documentation in this project must be managed with a dual-language system to ensure accessibility for both automated tools and human readers.

### File Structure

Every documentation file must have a corresponding Korean version:
- **Primary File**: `[filename].md` - For Claude Code and automated tools
- **Korean File**: `[filename]_KOR.md` - For human readers

### Examples
- `Test.md` ↔ `Test_KOR.md`
- `README.md` ↔ `README_KOR.md`
- `API_GUIDE.md` ↔ `API_GUIDE_KOR.md`

### Management Rules

1. **Synchronized Creation**: When creating a new documentation file, both versions must be created together
2. **Synchronized Updates**: Any modifications to one file must be reflected in its counterpart
3. **Synchronized Deletion**: When deleting documentation, both files must be removed
4. **1:1 Content Matching**: Content between files must be identical in meaning, only differing in language

### Purpose

- **Primary Files** (`*.md`): Optimized for Claude Code parsing and automated processing
- **Korean Files** (`*_KOR.md`): Human-readable documentation for Korean-speaking developers

### Implementation Checklist

When working with documentation:
- [ ] Create both language versions simultaneously
- [ ] Ensure content accuracy in both languages
- [ ] Maintain consistent formatting across versions
- [ ] Update both files when changes are needed
- [ ] Verify 1:1 content matching after updates

### File Naming Convention

- Use clear, descriptive names in English for the base filename
- Add `_KOR` suffix before the file extension for Korean versions
- Maintain consistent capitalization and formatting

### Quality Standards

- Ensure technical accuracy in both versions
- Use appropriate technical terminology for each language
- Maintain readability and clarity in Korean translations
- Keep formatting consistent between language versions