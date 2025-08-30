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

## 문서 자동화 스크립트

효율적인 문서 관리를 위한 Python 기반 크로스플랫폼 도구들:

### 빠른 명령어
```bash
# 스크립트 디렉토리로 이동
cd .claude/scripts

# 새 문서 쌍 생성 (영어 + 한국어)
python doc_manager.py create "기능-이름" --category architecture

# 모든 문서 인덱스 업데이트
python doc_manager.py index --update-all

# 문서 검증 및 자동 수정
python doc_manager.py validate --fix

# 완전한 문서 상태 검사
python doc_manager.py check

# 일반적인 문제 자동 수정
python doc_manager.py fix
```

### 토큰 최적화 효과
이 스크립트들은 Claude Code 토큰 사용량을 다음과 같이 줄입니다:
- **70%**: 템플릿 기반 문서 생성
- **60%**: 배치 처리 작업
- **50%**: 수동 검사 대신 자동 검증
- **40%**: 패턴 캐싱 및 재사용

### 사용 가능한 도구
- **doc_manager.py** - 모든 작업을 위한 메인 CLI 인터페이스
- **doc_create.py** - 템플릿을 사용한 문서 쌍 생성
- **doc_index.py** - INDEX 파일 생성 및 유지 관리
- 전체 사용법은 [스크립트 문서](.claude/scripts/README_KOR.md) 참조

## 문서 표준

⚠️ **중요**: 모든 문서는 이중 언어 시스템(영어 + 한국어)을 따라야 합니다.

### 문서 가이드라인
- **기본 파일** (`.md`): Claude Code 및 자동화 도구용 영어 콘텐츠
- **한국어 파일** (`_KOR.md`): 개발자가 읽기 위한 한국어 콘텐츠 전용
- **1:1 내용 매칭**: 두 버전 모두 동일한 의미를 가져야 함
- **동기화된 업데이트**: 변경사항은 두 파일에 모두 반영되어야 함

#### ⚠️ 중요: Claude Code 파일 참조 규칙
- **모든 비문서화 작업에서**: 항상 `.md` 파일 참조, `_KOR.md` 파일 절대 참조 금지
- **예외**: 문서 생성/번역 작업을 명시적으로 수행하는 경우만 해당
- **이유**: `_KOR.md` 파일은 개발자가 읽기 위해 설계됨, AI 소비용이 아님
- **자동화**: Claude Code 도구 및 스크립트는 일관성을 위해 `.md` 파일만 처리해야 함

자세한 규칙은 [문서 가이드라인](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES_KOR.md) 참조.

**문서 작업 시:**
1. **자동화 우선**: 모든 문서 작업에 `.claude/scripts/` 도구 사용
2. 항상 영어(`.md`)와 한국어(`_KOR.md`) 버전 모두 생성
3. 버전 간 내용 정확성과 일관성 보장
4. 파일명 규칙 준수: `filename.md` ↔ `filename_KOR.md`
5. 새 문서 생성 전 DOCUMENTATION_GUIDELINES.md 참조

### 필수 스크립트 사용
**모든 문서 작업 전에 반드시:**
```bash
cd .claude/scripts

# 새 문서: 수동 생성 대신 doc_manager.py 사용
python doc_manager.py create "문서-이름" --category [architecture|gamedesign|reference|guidelines]

# 업데이트: 일관성 유지를 위해 doc_index.py 사용
python doc_manager.py index --update-all

# 검증: 수동 확인 대신 내장 검사 사용
python doc_manager.py validate --fix
```

**스크립트 사용의 이점:**
- **자동 이중 언어 생성**: 수동 한국어 파일 생성 불필요
- **템플릿 일관성**: 적절한 메타데이터와 구조 보장
- **인덱스 동기화**: 모든 INDEX 파일 자동 업데이트
- **토큰 효율성**: 문서 작업에서 60-70% 감소

## 문서 인덱스

- [📚 메인 문서 인덱스](.claude/doc/INDEX_KOR.md) - 전체 문서 카탈로그
- [📖 문서 가이드라인](.claude/doc/guidelines/DOCUMENTATION_GUIDELINES_KOR.md)
- [🏗️ 프로젝트 아키텍처](.claude/doc/architecture/INDEX_KOR.md)
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

