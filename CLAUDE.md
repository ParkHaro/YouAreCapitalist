# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[🇰🇷 한국어 버전](./CLAUDE_KOR.md)

## Project Overview

Unity 6000.2.0f1 project "YouAreCapitalist" configured for mobile and PC platforms with Universal Render Pipeline (URP).

## Unity Development Commands

### Opening the Project
```bash
# Unity Editor is located at:
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe"

# Open project via command line:
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist"
```

### Build Commands
```bash
# Build for Windows (via Unity command line)
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -batchmode -quit -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist" -buildWindowsPlayer "Build\YouAreCapitalist.exe"

# Build for Android
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -batchmode -quit -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist" -buildTarget Android -executeMethod BuildScript.BuildAndroid
```

### Testing
```bash
# Run Unity tests
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -batchmode -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist" -runTests -testPlatform PlayMode -testResults "TestResults\playmode-results.xml"
```

## Project Architecture

### Render Pipeline Configuration
- **URP Version**: 17.2.0
- **PC Settings**: Assets/Settings/PC_RPAsset.asset, PC_Renderer.asset
- **Mobile Settings**: Assets/Settings/Mobile_RPAsset.asset, Mobile_Renderer.asset

### Assembly Structure
- **Assembly-CSharp**: Main gameplay code
- **Assembly-CSharp-Editor**: Editor-only scripts and tools
- **Target Framework**: .NET Standard 2.1

### Key Dependencies
- Universal Render Pipeline (com.unity.render-pipelines.universal: 17.2.0)
- Input System (com.unity.inputsystem: 1.14.1)
- Visual Scripting (com.unity.visualscripting: 1.9.7)
- Mobile support packages included

### Script Organization
- Game scripts: `Assets/Scripts/`
- Editor scripts: `Assets/Editor/`
- Input actions: `Assets/InputSystem_Actions.inputactions`

## Critical Documentation Rules

### Documentation Organization Structure
All documentation (except CLAUDE.md) must be stored in `.claude/doc/` directory:

```
.claude/
├── doc/
│   ├── guidelines/       # 개발 가이드라인
│   │   ├── DOCUMENTATION_GUIDELINES.md
│   │   └── DOCUMENTATION_GUIDELINES_KOR.md
│   ├── architecture/     # 아키텍처 문서
│   ├── api/             # API 문서
│   ├── guides/          # 사용자 가이드
│   └── reference/       # 참조 문서
└── CLAUDE.md           # 유일한 루트 문서
```

### Documentation Metadata
All `.md` files (except `_KOR` versions) must include metadata header for Claude Code:

```yaml
---
category: [guidelines|architecture|api|guides|reference]
tags: [unity, documentation, mobile, etc]
related: [linked-doc1.md, linked-doc2.md]
parent: parent-doc.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
priority: [high|medium|low]
---
```

### Document Navigation Structure
Every document must include a navigation section with:

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

### Document Hierarchy & Indexing
1. **Root Level**: CLAUDE.md (main index)
2. **Category Index**: Each category folder must have INDEX.md
3. **Cross-References**: Use metadata `related` field for connections
4. **Breadcrumb Trail**: Show document path in navigation

### Dual-Language Documentation System
Every documentation file MUST have a corresponding Korean version:
- Primary: `[filename].md` - For Claude Code parsing (includes metadata)
- Korean: `[filename]_KOR.md` - For human readers (no metadata)

When creating or modifying ANY documentation:
1. Always create/update both versions simultaneously
2. Ensure 1:1 content matching between languages
3. Never create one without the other
4. When deleting, remove both files
5. Store in appropriate `.claude/doc/` subdirectory

### Documentation Index
Key documentation links:
- [📚 Main Documentation Index](.claude/doc/INDEX.md) - Complete documentation catalog
- [Documentation Guidelines](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES.md)
- [Project Architecture](.claude/doc/architecture/INDEX.md)
- [API Reference](.claude/doc/api/INDEX.md)

### Cross-Language Link Rules
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

### Bidirectional Navigation
Every document pair must include navigation links:
```markdown
<!-- In document.md -->
[🇰🇷 한국어 버전](./document_KOR.md)

<!-- In document_KOR.md -->
[🇬🇧 English Version](./document.md)
```

## Development Considerations

### Platform-Specific Settings
- Mobile orientation: Auto-rotation enabled for all orientations
- Android minimum API: Check AndroidManifest for specific version
- Rendering: Linear color space, URP optimized for mobile

### Unity-Specific Patterns
- MonoBehaviour lifecycle: Awake → OnEnable → Start → Update → OnDisable → OnDestroy
- Coroutines for time-based operations
- ScriptableObjects for data containers
- Prefab workflow for reusable game objects

### Performance Guidelines
- Use object pooling for frequently instantiated objects
- Batch draw calls through SRP Batcher
- Profile using Unity Profiler before optimizing
- Mobile: Keep draw calls under 100-200, vertices under 100K

## File Locations

- Scenes: `Assets/Scenes/`
- Prefabs: Create in `Assets/Prefabs/` (if needed)
- Materials: Create in `Assets/Materials/` (if needed)
- Scripts: `Assets/Scripts/`
- Settings: `Assets/Settings/`

## Version Control Notes

- `.meta` files must be committed with their associated assets
- Never commit `Library/`, `Temp/`, `Logs/`, or `obj/` folders
- Project uses Unity 6000.2.0f1 - ensure version compatibility