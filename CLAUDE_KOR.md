# CLAUDE_KOR.md

이 파일은 이 저장소에서 코드 작업을 할 때 Claude Code (claude.ai/code)에 지침을 제공합니다.

[🇬🇧 English Version](./CLAUDE.md)

## 프로젝트 개요

Unity 6000.2.0f1 프로젝트 "YouAreCapitalist"는 모바일 및 PC 플랫폼용으로 Universal Render Pipeline (URP)으로 구성되어 있습니다.

## Unity 개발 명령어

### 프로젝트 열기
```bash
# Unity 에디터 위치:
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe"

# 명령줄로 프로젝트 열기:
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist"
```

### 빌드 명령어
```bash
# Windows용 빌드 (Unity 명령줄 사용)
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -batchmode -quit -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist" -buildWindowsPlayer "Build\YouAreCapitalist.exe"

# Android용 빌드
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -batchmode -quit -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist" -buildTarget Android -executeMethod BuildScript.BuildAndroid
```

### 테스트
```bash
# Unity 테스트 실행
"C:\Program Files\Unity\Hub\Editor\6000.2.0f1\Editor\Unity.exe" -batchmode -projectPath "C:\Users\haro7\Projects\Unity\YouAreCapitalist" -runTests -testPlatform PlayMode -testResults "TestResults\playmode-results.xml"
```

## 프로젝트 구조

### 렌더 파이프라인 설정
- **URP 버전**: 17.2.0
- **PC 설정**: Assets/Settings/PC_RPAsset.asset, PC_Renderer.asset
- **모바일 설정**: Assets/Settings/Mobile_RPAsset.asset, Mobile_Renderer.asset

### 어셈블리 구조
- **Assembly-CSharp**: 메인 게임플레이 코드
- **Assembly-CSharp-Editor**: 에디터 전용 스크립트 및 도구
- **타겟 프레임워크**: .NET Standard 2.1

### 주요 의존성
- Universal Render Pipeline (com.unity.render-pipelines.universal: 17.2.0)
- Input System (com.unity.inputsystem: 1.14.1)
- Visual Scripting (com.unity.visualscripting: 1.9.7)
- 모바일 지원 패키지 포함

### 스크립트 구성
- 게임 스크립트: `Assets/Scripts/`
- 에디터 스크립트: `Assets/Editor/`
- 입력 액션: `Assets/InputSystem_Actions.inputactions`

## 빠른 참조

- [📁 경로 단축어](.claude/doc/reference/PATH_SHORTCUTS_KOR.md) - 문서 경로 약어
- [📝 Git 로그 명령어](.claude/doc/reference/GIT_LOG_DOCUMENTATION_KOR.md) - 자동 git 히스토리 문서화

## 문서 표준

⚠️ **중요**: 모든 문서는 이중 언어 시스템(영어 + 한국어)을 따라야 합니다.
자세한 규칙은 [문서 가이드라인](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES_KOR.md) 참조.

## 문서 인덱스

- [📚 메인 문서 인덱스](.claude/doc/INDEX_KOR.md) - 전체 문서 카탈로그
- [📖 문서 가이드라인](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES_KOR.md)
- [🏗️ 프로젝트 아키텍처](.claude/doc/architecture/INDEX_KOR.md)
- [🔌 API 참조](.claude/doc/api/INDEX_KOR.md)
- [🎮 게임 디자인 문서](.claude/doc/gamedesign/INDEX_KOR.md)

## 개발 고려사항

### 플랫폼별 설정
- 모바일 방향: 모든 방향으로 자동 회전 활성화
- Android 최소 API: AndroidManifest에서 특정 버전 확인
- 렌더링: 선형 색 공간, 모바일용 URP 최적화

### Unity 특정 패턴
- MonoBehaviour 수명 주기: Awake → OnEnable → Start → Update → OnDisable → OnDestroy
- 시간 기반 작업용 코루틴
- 데이터 컨테이너용 ScriptableObjects
- 재사용 가능한 게임 오브젝트용 프리팹 워크플로

### 성능 가이드라인
- 자주 인스턴스화되는 오브젝트에 오브젝트 풀링 사용
- SRP Batcher를 통한 드로우 콜 배치
- 최적화 전 Unity 프로파일러 사용
- 모바일: 드로우 콜 100-200 이하, 버텍스 100K 이하 유지

## 파일 위치

- 씬: `Assets/Scenes/`
- 프리팹: `Assets/Prefabs/`에 생성 (필요시)
- 머티리얼: `Assets/Materials/`에 생성 (필요시)
- 스크립트: `Assets/Scripts/`
- 설정: `Assets/Settings/`

## 버전 관리 주의사항

- `.meta` 파일은 연관된 에셋과 함께 커밋
- `Library/`, `Temp/`, `Logs/`, `obj/` 폴더는 절대 커밋 금지
- 프로젝트는 Unity 6000.2.0f1 사용 - 버전 호환성 확인 필요

