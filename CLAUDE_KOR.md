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

## 중요 문서화 규칙

### 문서 구조 체계
모든 문서(CLAUDE.md 제외)는 `.claude/doc/` 디렉토리에 저장되어야 합니다:

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

### 문서 메타데이터
모든 `.md` 파일(`_KOR` 버전 제외)은 Claude Code용 메타데이터 헤더를 포함해야 합니다:

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

### 문서 네비게이션 구조
모든 문서는 네비게이션 섹션을 포함해야 합니다:

```markdown
## 📍 네비게이션

[↩️ 상위 문서](./parent-document_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

### 🔗 관련 문서
- [관련 문서 1](./related1_KOR.md) - 간단한 설명
- [관련 문서 2](./related2_KOR.md) - 간단한 설명

### 📚 이 섹션의 문서들
- [하위 문서 1](./child1_KOR.md)
- [하위 문서 2](./child2_KOR.md)
```

### 문서 계층 구조 및 인덱싱
1. **루트 레벨**: CLAUDE.md (메인 인덱스)
2. **카테고리 인덱스**: 각 카테고리 폴더에 INDEX.md 필수
3. **상호 참조**: 메타데이터 `related` 필드로 연결
4. **경로 표시**: 네비게이션에 문서 경로 표시

### 이중 언어 문서 시스템
모든 문서 파일은 반드시 한국어 버전을 가져야 합니다:
- 기본: `[filename].md` - Claude Code 파싱용 (메타데이터 포함)
- 한국어: `[filename]_KOR.md` - 사용자 읽기용 (메타데이터 없음)

문서 생성이나 수정 시:
1. 항상 두 버전을 동시에 생성/업데이트
2. 언어 간 1:1 콘텐츠 매칭 보장
3. 한 버전만 생성 금지
4. 삭제 시 두 파일 모두 제거
5. 적절한 `.claude/doc/` 하위 디렉토리에 저장

### 문서 인덱스
주요 문서 링크:
- [📚 메인 문서 인덱스](.claude/doc/INDEX_KOR.md) - 전체 문서 카탈로그
- [문서 가이드라인](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES_KOR.md)
- [프로젝트 아키텍처](.claude/doc/architecture/INDEX_KOR.md)
- [API 참조](.claude/doc/api/INDEX_KOR.md)

### 언어 간 링크 규칙
**중요**: 링크는 언어 버전을 준수해야 합니다:
- `.md` 파일에서: 다른 `.md` 파일로 링크
- `_KOR.md` 파일에서: 다른 `_KOR.md` 파일로 링크

예시:
```markdown
<!-- README.md에서 -->
See [API Guide](.claude/doc/api/API_GUIDE.md)

<!-- README_KOR.md에서 -->
참조: [API 가이드](.claude/doc/api/API_GUIDE_KOR.md)
```

### 양방향 네비게이션
모든 문서 쌍은 네비게이션 링크를 포함해야 합니다:
```markdown
<!-- document.md에서 -->
[🇰🇷 한국어 버전](./document_KOR.md)

<!-- document_KOR.md에서 -->
[🇬🇧 English Version](./document.md)
```

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