# Vault 표준화 자동화 가이드

> 생성일: 2025-11-30
> Obsidian vault의 frontmatter, 태그, 연결성을 자동으로 표준화하는 도구

## 📋 목차

1. [개요](#개요)
2. [사용법](#사용법)
3. [Phase별 설명](#phase별-설명)
4. [예제](#예제)
5. [주의사항](#주의사항)
6. [FAQ](#faq)

## 🎯 개요

이 스크립트는 DAE Second Brain vault의 다음 항목을 표준화합니다:

- **Frontmatter Type**: 한글/영어 혼용 → 영어 통일
- **Tags**: 한글 태그 → 영어 변환, 네이밍 규칙 적용
- **필수 필드**: created, updated, title, aliases 자동 추가
- **Related 섹션**: 파일 간 연결성 강화

### 주요 기능

✅ **안전한 처리**: 기본적으로 Dry-run 모드 (테스트만)
✅ **선택적 적용**: Phase별, 영역별 선택 가능
✅ **자동 백업**: Git과 함께 사용 권장
✅ **변경 내역**: 모든 변경사항 상세 로깅

## 🚀 사용법

### 1. 기본 사용법

```bash
cd /Users/qraft_hongjinyoung/DAE-Second-Brain/automation

# Phase 1 (Type 표준화) 테스트
python vault_standardizer.py --phase 1 --dry-run

# Phase 2 (Tags 표준화) 실제 적용
python vault_standardizer.py --phase 2 --apply

# 특정 영역만 처리
python vault_standardizer.py --phase 1 --area "30-Flow/Life-Insights/Personal" --dry-run

# 모든 Phase 한번에
python vault_standardizer.py --all --dry-run
```

### 2. 권장 워크플로우

```bash
# Step 1: Git 백업
cd /Users/qraft_hongjinyoung/DAE-Second-Brain
git add .
git commit -m "✨ Before vault standardization"

# Step 2: 샘플 영역 테스트 (Dry-run)
cd automation
python vault_standardizer.py --phase 1 --area "30-Flow/Life-Insights/Personal" --dry-run

# Step 3: 결과 확인 후 실제 적용
python vault_standardizer.py --phase 1 --area "30-Flow/Life-Insights/Personal" --apply

# Step 4: Obsidian에서 수동 확인

# Step 5: 전체 적용
python vault_standardizer.py --phase 1 --apply
python vault_standardizer.py --phase 2 --apply
python vault_standardizer.py --phase 3 --apply
python vault_standardizer.py --phase 4 --apply

# Step 6: Git 커밋
cd ..
git add .
git commit -m "✨ Apply vault standardization (Phase 1-4)"
```

## 📦 Phase별 설명

### Phase 1: Type 표준화

**목적**: Frontmatter의 `type` 필드를 표준화

**변환 규칙**:
```
주간회고 → weekly-reflection
daily-insight → insight
daily-reflection → reflection
일일회고 → reflection
하루일기 → insight
```

**예시**:
```yaml
# Before
---
type: 주간회고
---

# After
---
type: weekly-reflection
---
```

### Phase 2: Tags 표준화

**목적**: 태그를 영어로 통일하고 네이밍 규칙 적용

**변환 규칙**:
```
커리어 → career
문제해결 → problem-solving
데이터거버넌스 → data-governance
구조화 → structuring
문서화 → documentation
의사소통 → communication
협업 → collaboration
기술전파 → knowledge-sharing
비용 최적화 → cost-optimization
성능개선 → performance-optimization
(... 전체 목록은 스크립트 참조)
```

**예시**:
```yaml
# Before
---
tags: [커리어, 문제해결, 데이터거버넌스]
---

# After
---
tags: [career, problem-solving, data-governance]
---
```

### Phase 3: 필수 필드 추가

**목적**: 누락된 frontmatter 필드 자동 추가

**추가 필드**:
- `created`: 파일 생성일 (파일 시스템 기준)
- `updated`: 파일 수정일 (파일 시스템 기준)
- `title`: 파일명 기반
- `aliases`: 빈 배열 (수동 추가 가능)

**예시**:
```yaml
# Before
---
type: insight
---

# After
---
type: insight
created: "2025-08-28"
updated: "2025-11-30"
title: "크래프트 첫 출근"
aliases: []
---
```

### Phase 4: Related 섹션 생성

**목적**: 파일 간 연결성 강화를 위한 섹션 추가

**추가 내용**:
```markdown
---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

```

**참고**: 이 Phase는 템플릿만 추가합니다. 실제 링크는 수동으로 추가하거나 Phase 5에서 자동 생성됩니다.

### Phase 5: 백링크 강화 (개발 예정)

**목적**: 태그/내용 기반 자동 링크 생성

## 📝 예제

### 예제 1: Life-Insights/Personal 영역 표준화

```bash
# 1. 테스트
python vault_standardizer.py --phase 1 --area "30-Flow/Life-Insights/Personal" --dry-run

# 출력 예시:
# ============================================================
# Phase 1 실행: 66개 파일
# 영역: 30-Flow/Life-Insights/Personal
# 모드: DRY RUN (테스트)
# ============================================================
#
# 📄 30-Flow/Life-Insights/Personal/크래프트-첫-출근.md
#   • Type: 'daily-insight' → 'insight'
#   [DRY RUN] 저장할 내용:
#   ---
#   title: 크래프트 첫 출근
#   type: insight
#   ...

# 2. 결과 확인 후 적용
python vault_standardizer.py --phase 1 --area "30-Flow/Life-Insights/Personal" --apply
```

### 예제 2: 전체 vault 표준화 (Phase 1-3)

```bash
# Git 백업
git add .
git commit -m "🔖 Before standardization"

# Phase 1: Type
python vault_standardizer.py --phase 1 --dry-run
python vault_standardizer.py --phase 1 --apply

# Phase 2: Tags
python vault_standardizer.py --phase 2 --dry-run
python vault_standardizer.py --phase 2 --apply

# Phase 3: Fields
python vault_standardizer.py --phase 3 --apply

# Git 커밋
git add .
git commit -m "✨ Standardize vault (Type + Tags + Fields)"
```

## ⚠️ 주의사항

### 1. 백업 필수

**반드시 Git 커밋 후 실행하세요!**

```bash
git add .
git commit -m "Backup before standardization"
```

### 2. Dry-run으로 먼저 테스트

- `--dry-run`은 **기본값**입니다
- 실제 적용하려면 반드시 `--apply` 옵션 필요
- 결과를 확인한 후 적용하세요

### 3. 영역별 단계 적용

한번에 전체 vault를 처리하기보다는:

1. **샘플 영역** (예: Life-Insights/Personal) 먼저 테스트
2. 결과 확인
3. 전체 적용

### 4. Obsidian 재시작

- 파일 변경 후 Obsidian이 자동으로 반영하지 않을 수 있음
- Obsidian을 재시작하거나 Reload (Ctrl+R) 실행

### 5. 수동 확인 필요 항목

자동화가 100% 정확하지 않을 수 있는 부분:

- **비표준 타입**: 경고만 표시됨, 수동 검토 필요
- **컨텍스트 태그**: 내용 기반 태그는 제한적
- **Related 링크**: 자동 생성은 Phase 5에서 구현 예정

## 🔧 커스터마이징

### 태그 매핑 추가

`vault_standardizer.py`의 `TAG_MAPPING` 딕셔너리에 추가:

```python
TAG_MAPPING = {
    # 기존 매핑...
    "새로운한글태그": "new-english-tag",
}
```

### Type 매핑 추가

`TYPE_MAPPING` 딕셔너리에 추가:

```python
TYPE_MAPPING = {
    # 기존 매핑...
    "새로운타입": "standard-type",
}
```

## 📊 통계 보기

스크립트 실행 후 자동으로 통계가 표시됩니다:

```
============================================================
완료!
  총 파일: 66
  처리됨: 45
  건너뜀: 21
  오류: 0
  총 변경: 135
============================================================
```

## ❓ FAQ

### Q1. Dry-run 모드가 무엇인가요?

A. 실제로 파일을 변경하지 않고, 변경될 내용을 미리 보여주는 테스트 모드입니다. 기본값이므로 안심하고 실행할 수 있습니다.

### Q2. 실행 중 오류가 나면?

A. 스크립트는 개별 파일 오류를 건너뛰고 계속 진행합니다. 오류 파일은 수동으로 확인하세요.

### Q3. 특정 파일만 처리하고 싶어요.

A. `--area` 옵션으로 디렉토리를 지정하거나, 스크립트를 수정하여 특정 파일 필터링을 추가하세요.

### Q4. 원래대로 되돌리고 싶어요.

A. Git을 사용했다면:
```bash
git reset --hard HEAD~1  # 마지막 커밋 취소
```

### Q5. Phase는 순서대로 실행해야 하나요?

A. 아니요. 독립적으로 실행 가능합니다. 다만 Phase 1-3은 순서대로 하는 것을 권장합니다.

## 📚 추가 자료

- [표준화 계획 문서](../90-Meta/VAULT_STANDARDIZATION_PLAN.md)
- [Claude Code 설정]](../.claude/CLAUDE.md)

## 🛠️ 개발 정보

- **언어**: Python 3.8+
- **의존성**: PyYAML
- **라이선스**: MIT
- **작성자**: Claude Code (Sonnet 4.5)
- **버전**: 1.0

---

**마지막 업데이트**: 2025-11-30
