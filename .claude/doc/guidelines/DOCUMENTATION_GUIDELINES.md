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

## Documentation Organization Structure

All documentation (except CLAUDE.md) must be stored in `.claude/doc/` directory:

```
.claude/
├── doc/
│   ├── guidelines/       # Development guidelines
│   ├── architecture/     # Architecture documentation
│   ├── api/             # API documentation
│   ├── gamedesign/      # Game design documentation
│   │   ├── mechanics/   # Game mechanics
│   │   ├── systems/     # Game systems
│   │   ├── levels/      # Level design
│   │   └── economy/     # Economy system
│   ├── guides/          # User guides
│   └── reference/       # Reference documentation
└── CLAUDE.md           # Root documentation file
```

## Documentation Metadata

All `.md` files (except `_KOR` versions) must include metadata header:

```yaml
---
category: [guidelines|architecture|api|guides|reference|gamedesign]
tags: [unity, documentation, mobile, etc]
related: [linked-doc1.md, linked-doc2.md]
parent: parent-doc.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
priority: [high|medium|low]
---
```

## Document Navigation Structure

Every document must include a navigation section:

```markdown
## 📍 Navigation

[↩️ Back to Parent](./parent-document.md) | [🏠 Home](../../CLAUDE.md)

### 🔗 Related Documents
- [Related Doc 1](./related1.md) - Brief description
- [Related Doc 2](./related2.md) - Brief description

### 📚 In This Section
- [Child Doc 1](./child1.md)
- [Child Doc 2](./child2.md)
```

## Document Hierarchy & Indexing

1. **Root Level**: CLAUDE.md (main index)
2. **Category Index**: Each category folder must have INDEX.md
3. **Cross-References**: Use metadata `related` field for connections
4. **Breadcrumb Trail**: Show document path in navigation

## Cross-Language Link Rules

**CRITICAL**: Links must respect language versions:
- In `.md` files: Link to other `.md` files
- In `_KOR.md` files: Link to other `_KOR.md` files

Example:
```markdown
<!-- In README.md -->
See [API Guide](.claude/doc/api/API_GUIDE.md)

<!-- In README_KOR.md -->
참조: [API 가이드](.claude/doc/api/API_GUIDE_KOR.md)
```

## Game Design Documentation Guidelines

Game design documents in `claude_gamedesign/` folder:
- **Cross-Linking**: Actively link to related mechanics, systems, and features
- **Hierarchical Structure**: Use subfolders for organizing complex systems
- **Categories**: mechanics/, systems/, levels/, economy/, ui-ux/, narrative/
- **Version Control**: Track design iterations and decisions
- **Visual Assets**: Reference concept art and prototypes in `assets/` subfolder

## CLAUDE.md Management Principles

### Core Principles
- **Keep It Essential**: Only include critical project information
- **Link to Details**: Use links for detailed information
- **Quick Reference**: Should serve as a quick reference guide
- **No Duplication**: Avoid duplicating content from subdocuments

### What Belongs in CLAUDE.md
- Project overview (1-2 lines)
- Essential Unity commands
- Critical file locations
- Documentation index links
- Path shortcuts reference

### What Should Be Moved to Subdocuments
- Detailed command explanations → `/reference/`
- Extended guidelines → `/guidelines/`
- Complex configurations → `/architecture/`
- Step-by-step procedures → `/guides/`

## Git Commit Guidelines

### Commit Message Format
When creating git commits for this project:

1. **Use conventional commit format**: `type: description`
2. **Types**: feat, fix, docs, style, refactor, test, chore
3. **Keep subject line under 50 characters**
4. **Provide detailed body for complex changes**
5. **Reference issues when applicable**

### Important Note
**DO NOT** include Claude Code signatures or co-authorship lines in commit messages:
- ❌ Never add: `🤖 Generated with Claude Code`
- ❌ Never add: `Co-Authored-By: Claude <noreply@anthropic.com>`
- ✅ Keep commits clean and professional
- ✅ Focus on describing the actual changes made