# 문서 경로 단축어

[🇬🇧 English Version](./PATH_SHORTCUTS.md)

## 📍 네비게이션

[↩️ 참조 문서로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../../CLAUDE_KOR.md)

## 경로 약어

문서 경로를 참조할 때 사용할 수 있는 단축어:

- **`claude_root`** = `.claude/` - Claude 루트 디렉토리
- **`claude_doc`** = `.claude/doc/` - 메인 문서 디렉토리
- **`claude_guidelines`** = `.claude/doc/guidelines/` - 개발 가이드라인
- **`claude_arch`** = `.claude/doc/architecture/` - 아키텍처 문서
- **`claude_api`** = `.claude/doc/api/` - API 문서
- **`claude_gamedesign`** = `.claude/doc/gamedesign/` - 게임 디자인 문서
- **`claude_guides`** = `.claude/doc/guides/` - 사용자 가이드
- **`claude_ref`** = `.claude/doc/reference/` - 참조 문서
- **`claude_project_log`** = `.claude/project_log/` - 프로젝트 활동 로그

## 사용 예시

### 문서에서
```markdown
// 대신: .claude/doc/gamedesign/mechanics.md
// 사용: claude_gamedesign/mechanics.md

// 대신: .claude/doc/architecture/system-design.md
// 사용: claude_arch/system-design.md
```

### 명령어에서
```bash
# 단축어를 사용한 문서 참조
cd claude_doc
ls claude_gamedesign
```

### 링크에서
```markdown
[게임 메커닉](claude_gamedesign/mechanics.md) 참조
[아키텍처 가이드](claude_arch/system-design.md) 참고
```

## 장점

1. **간결성**: 짧은 경로로 타이핑 감소 및 가독성 향상
2. **일관성**: 모든 문서에서 표준 단축어 사용
3. **유지보수성**: 디렉토리 구조 변경 시 쉬운 업데이트
4. **명확성**: 자체 설명적인 단축어로 콘텐츠 유형 표시

## 모범 사례

- 내부 문서 참조 시 항상 단축어 사용
- 새로운 단축어는 이 파일에 문서화
- 모든 언어에서 일관성 유지
- 외부 파일에서 참조 시 절대 경로 사용