# 문서 가이드라인

[🇬🇧 English Version](./DOCUMENTATION_GUIDELINES.md)

## 📍 네비게이션

[↩️ 가이드라인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../../CLAUDE_KOR.md)

## 이중 언어 문서 시스템

이 프로젝트의 모든 문서는 자동화 도구와 사용자 모두의 접근성을 보장하기 위해 이중 언어 시스템으로 관리되어야 합니다.

### 파일 구조

모든 문서 파일은 해당하는 한국어 버전을 가져야 합니다:
- **기본 파일**: `[filename].md` - Claude Code 및 자동화 도구용
- **한국어 파일**: `[filename]_KOR.md` - 사용자 읽기용

### 예시
- `Test.md` ↔ `Test_KOR.md`
- `README.md` ↔ `README_KOR.md`
- `API_GUIDE.md` ↔ `API_GUIDE_KOR.md`

### 관리 규칙

1. **동기화된 생성**: 새 문서 파일을 생성할 때 두 버전을 함께 생성해야 합니다
2. **동기화된 업데이트**: 한 파일의 수정 사항은 반드시 해당 파일에 반영되어야 합니다
3. **동기화된 삭제**: 문서 삭제 시 두 파일 모두 제거해야 합니다
4. **1:1 콘텐츠 매칭**: 파일 간 콘텐츠는 의미상 동일해야 하며, 언어만 다릅니다

### 목적

- **기본 파일** (`*.md`): Claude Code 파싱 및 자동화 처리에 최적화
- **한국어 파일** (`*_KOR.md`): 한국어 사용 개발자를 위한 가독성 있는 문서

### 구현 체크리스트

문서 작업 시:
- [ ] 두 언어 버전을 동시에 생성
- [ ] 두 언어의 콘텐츠 정확성 보장
- [ ] 버전 간 일관된 포맷 유지
- [ ] 변경 필요 시 두 파일 모두 업데이트
- [ ] 업데이트 후 1:1 콘텐츠 매칭 확인

### 파일 명명 규칙

- 기본 파일명은 명확하고 설명적인 영어 사용
- 한국어 버전은 파일 확장자 앞에 `_KOR` 접미사 추가
- 일관된 대소문자 및 포맷 유지

### 품질 기준

- 두 버전 모두 기술적 정확성 보장
- 각 언어에 적합한 기술 용어 사용
- 한국어 번역의 가독성과 명확성 유지
- 언어 버전 간 일관된 포맷 유지

## 문서 구조 체계

모든 문서(CLAUDE.md 제외)는 `.claude/doc/` 디렉토리에 저장되어야 합니다:

```
.claude/
├── doc/
│   ├── guidelines/       # 개발 가이드라인
│   ├── architecture/     # 아키텍처 문서
│   ├── api/             # API 문서
│   ├── gamedesign/      # 게임 디자인 문서
│   │   ├── mechanics/   # 게임 메커닉
│   │   ├── systems/     # 게임 시스템
│   │   ├── levels/      # 레벨 디자인
│   │   └── economy/     # 경제 시스템
│   ├── guides/          # 사용자 가이드
│   └── reference/       # 참조 문서
└── CLAUDE.md           # 루트 문서 파일
```

## 문서 메타데이터

모든 `.md` 파일(`_KOR` 버전 제외)은 메타데이터 헤더를 포함해야 합니다:

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

## 문서 네비게이션 구조

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

## 문서 계층 구조 및 인덱싱

1. **루트 레벨**: CLAUDE.md (메인 인덱스)
2. **카테고리 인덱스**: 각 카테고리 폴더에 INDEX.md 필수
3. **상호 참조**: 메타데이터 `related` 필드로 연결
4. **경로 표시**: 네비게이션에 문서 경로 표시

## 언어 간 링크 규칙

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

## 게임 디자인 문서 작성 지침

`claude_gamedesign/` 폴더의 게임 디자인 문서:
- **교차 링킹**: 관련 메커닉, 시스템, 기능과 적극적으로 연결
- **계층 구조**: 복잡한 시스템 정리를 위한 하위 폴더 사용
- **카테고리**: mechanics/, systems/, levels/, economy/, ui-ux/, narrative/
- **버전 관리**: 디자인 반복 및 결정 추적
- **비주얼 에셋**: 컨셉트 아트와 프로토타입을 `assets/` 하위 폴더에 참조

## CLAUDE.md 관리 원칙

### 핵심 원칙
- **필수 정보만 유지**: 중요한 프로젝트 정보만 포함
- **상세 정보는 링크로**: 상세 정보는 링크 사용
- **빠른 참조**: 빠른 참조 가이드 역할
- **중복 방지**: 하위 문서와 내용 중복 방지

### CLAUDE.md에 포함될 내용
- 프로젝트 개요 (1-2줄)
- 필수 Unity 명령어
- 중요 파일 위치
- 문서 인덱스 링크
- 경로 단축어 참조

### 하위 문서로 이동할 내용
- 상세 명령어 설명 → `/reference/`
- 확장된 가이드라인 → `/guidelines/`
- 복잡한 설정 → `/architecture/`
- 단계별 절차 → `/guides/`

## Git 커밋 가이드라인

### 커밋 메시지 형식
이 프로젝트에서 git 커밋을 생성할 때:

1. **관례적 커밋 형식 사용**: `type: description`
2. **타입**: feat, fix, docs, style, refactor, test, chore
3. **제목 줄은 50자 이하로 유지**
4. **복잡한 변경사항은 상세한 본문 제공**
5. **해당되는 경우 이슈 참조**

### 중요 사항
커밋 메시지에 Claude Code 서명이나 공동 저자 줄을 **포함하지 마세요**:
- ❌ 절대 추가하지 말 것: `🤖 Generated with Claude Code`
- ❌ 절대 추가하지 말 것: `Co-Authored-By: Claude <noreply@anthropic.com>`
- ✅ 깔끔하고 전문적인 커밋 유지
- ✅ 실제 변경사항 설명에 집중