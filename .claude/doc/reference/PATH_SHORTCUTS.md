---
category: reference
tags: [paths, shortcuts, navigation, claude]
related: [DOCUMENTATION_GUIDELINES.md]
parent: INDEX.md
created: 2025-08-28
updated: 2025-08-28
priority: high
---

# Documentation Path Shortcuts

[🇰🇷 한국어 버전](./PATH_SHORTCUTS_KOR.md)

## 📍 Navigation

[↩️ Back to Reference](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## Path Abbreviations

These shortcuts can be used when referencing documentation paths:

- **`claude_root`** = `.claude/` - Claude root directory
- **`claude_doc`** = `.claude/doc/` - Main documentation directory
- **`claude_guidelines`** = `.claude/doc/guidelines/` - Development guidelines
- **`claude_arch`** = `.claude/doc/architecture/` - Architecture documentation
- **`claude_api`** = `.claude/doc/api/` - API documentation
- **`claude_gamedesign`** = `.claude/doc/gamedesign/` - Game design documentation
- **`claude_guides`** = `.claude/doc/guides/` - User guides
- **`claude_ref`** = `.claude/doc/reference/` - Reference documentation
- **`claude_project_log`** = `.claude/project_log/` - Project activity logs

## Usage Examples

### In Documentation
```markdown
// Instead of: .claude/doc/gamedesign/mechanics.md
// Use: claude_gamedesign/mechanics.md

// Instead of: .claude/doc/architecture/system-design.md
// Use: claude_arch/system-design.md
```

### In Commands
```bash
# Reference documentation using shortcuts
cd claude_doc
ls claude_gamedesign
```

### In Links
```markdown
See [Game Mechanics](claude_gamedesign/mechanics.md)
Refer to [Architecture Guide](claude_arch/system-design.md)
```

## Benefits

1. **Brevity**: Shorter paths reduce typing and improve readability
2. **Consistency**: Standard shortcuts across all documentation
3. **Maintainability**: Easy to update if directory structure changes
4. **Clarity**: Self-documenting shortcuts indicate content type

## Best Practices

- Always use shortcuts in internal documentation references
- Document any new shortcuts in this file
- Maintain consistency across all languages
- Use absolute paths when referencing from external files