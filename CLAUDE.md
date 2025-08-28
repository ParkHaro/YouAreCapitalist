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

## Quick References

- [📁 Path Shortcuts](.claude/doc/reference/PATH_SHORTCUTS.md) - Documentation path abbreviations
- [📝 Git Log Commands](.claude/doc/reference/GIT_LOG_DOCUMENTATION.md) - Automated git history documentation

## Documentation Standards

⚠️ **Important**: All documentation must follow dual-language system (English + Korean).
See [Documentation Guidelines](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES.md) for complete rules.

## Documentation Index

- [📚 Main Documentation Index](.claude/doc/INDEX.md) - Complete documentation catalog
- [📖 Documentation Guidelines](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES.md)
- [🏗️ Project Architecture](.claude/doc/architecture/INDEX.md)
- [🔌 API Reference](.claude/doc/api/INDEX.md)
- [🎮 Game Design Documents](.claude/doc/gamedesign/INDEX.md)

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

