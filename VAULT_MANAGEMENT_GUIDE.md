---
type: guide
category: documentation
created: 2025-11-28
---

# DAE Second Brain - Vault Management Guide

Second Brain이 제 역할을 하도록 관리하는 종합 가이드

---

## 🎯 목표

문서들이 **적절하게 발견되고 연결**되어 Second Brain이 진정한 외부 뇌 역할을 하도록 함

---

## 🛠️ 도구 개요

### 1. **validate_vault.py** - 검증
현재 상태를 분석하고 문제를 발견

```bash
python3 validate_vault.py
```

**검증 항목**:
- ✅ 네트워크 구조 (backlinks, forward links, orphans, hubs)
- ✅ 중복 파일
- ✅ 깨진 링크
- ✅ 메타데이터 누락

**출력**:
- 콘솔에 요약 리포트
- `vault_validation_report.json` (상세 데이터)

---

### 2. **cleanup_vault.py** - 정리
발견된 문제를 자동으로 해결

```bash
# Dry-run (변경 없이 계획만 보기)
python3 cleanup_vault.py

# 실제 실행
python3 cleanup_vault.py --apply
```

**정리 작업**:
- 🗑️ 중복 파일 삭제 (내용 비교 기반)
- 📝 YAML 메타데이터 자동 수정
- 🔗 README에 프로젝트 링크 추가
- 📚 Documentation 섹션 생성

---

### 3. **second_brain_agent.py** - 큐레이션
Second Brain의 발견성과 연결성을 향상

```bash
# 분석 및 제안만
python3 second_brain_agent.py

# 제안 + 자동 개선
python3 second_brain_agent.py --enhance

# 제안 + 자동 개선 실행
python3 second_brain_agent.py --enhance --apply
```

**큐레이션 기능**:
- 🔍 발견성 분석 (각 문서의 발견 가능성 점수)
- 🔗 연결 제안 (관련 문서 간 링크 제안)
- 🌟 Hub 제안 (클러스터에 Hub 페이지 생성)
- 📊 종합 리포트 생성

**출력**:
- 콘솔에 분석 결과
- `second_brain_report.md` (상세 제안)

---

## 📋 워크플로우

### 주간 유지보수 (매주 1회)

```bash
# 1. 현재 상태 검증
python3 validate_vault.py

# 2. 문제 자동 정리
python3 cleanup_vault.py --apply

# 3. Second Brain 큐레이션
python3 second_brain_agent.py

# 4. 리포트 확인
# - vault_validation_report.json
# - second_brain_report.md
```

### 월간 최적화 (매월 1회)

```bash
# 1. 검증 + 정리
python3 validate_vault.py
python3 cleanup_vault.py --apply

# 2. 제안 검토 및 적용
python3 second_brain_agent.py

# 리포트 확인 후 high-confidence 제안 수동 적용

# 3. 자동 개선 (선택적)
python3 second_brain_agent.py --enhance --apply
```

### 새 프로젝트 추가 후

```bash
# Notion에서 임포트한 후
python3 import_qraft_notion_fixed.py

# 즉시 큐레이션
python3 second_brain_agent.py

# 제안 확인 및 링크 추가
```

---

## 📊 발견성 점수 이해하기

Second Brain Agent가 계산하는 발견성 점수:

| 점수 | 상태 | 설명 |
|------|------|------|
| 20+ | 🌟 Excellent | Hub 페이지, 많은 backlinks |
| 10-19 | ✅ Good | 적절히 연결됨 |
| 0-9 | ⚠️ Needs improvement | 일부 연결 부족 |
| < 0 | ❌ Poor | 고아 페이지, 발견 어려움 |

**점수 계산 요소**:
- Backlinks: +2점 per link (최대 20점)
- Outgoing links: +1점 per link (최대 10점)
- Hub에 포함: +10점
- 메타데이터 완성: +5점
- 태그 존재: +5점
- 충분한 내용: +5점

**페널티**:
- No backlinks (orphan): -10점
- No outgoing links: -5점
- Missing metadata: -5점
- No tags: -3점
- Very short content: -5점
- Not in hub: -8점

---

## 🎯 모범 사례

### 1. 새 문서 작성 시

```markdown
---
type: concept|experience|pattern
category: relevant-category
tags: [tag1, tag2, tag3]
created: YYYY-MM-DD
---

# 제목

## 내용
(최소 200자 이상)

## 🔗 Related
- [[관련-문서-1]]
- [[관련-문서-2]]
```

### 2. Hub 페이지 관리

- 각 주요 카테고리에 Hub 페이지 유지
- Hub는 해당 영역의 모든 문서 링크
- 주기적으로 새 문서 추가

### 3. 링크 전략

- **문서 내에서 언급될 때 링크**: `[[문서-제목]]`
- **Related 섹션**: 간접적으로 관련된 문서
- **Hub 페이지**: 같은 카테고리의 모든 문서

---

## 🔄 자동화 스크립트

### Notion 임포트

```bash
# Qraft 업무리스트 임포트
python3 import_qraft_notion_fixed.py
```

**특징**:
- ✅ 재귀적으로 모든 중첩 블록 가져오기
- ✅ 이미지, 파일, 북마크 지원
- ✅ 적절한 들여쓰기 유지
- ✅ 중복 방지 (notion_id 기반)

### 검증 + 정리 자동화

```bash
#!/bin/bash
# weekly_maintenance.sh

cd "/Users/qraft_hongjinyoung/DAE-Second-Brain"

echo "🔍 Validating vault..."
python3 validate_vault.py

echo ""
echo "🧹 Cleaning up..."
python3 cleanup_vault.py --apply

echo ""
echo "🧠 Curating Second Brain..."
python3 second_brain_agent.py

echo ""
echo "✅ Weekly maintenance complete!"
echo "📄 Check second_brain_report.md for suggestions"
```

---

## 📈 성과 지표

### 월별 추적

```bash
# 스크립트 실행 전후로 비교
python3 validate_vault.py > validation_before.txt

# ... 개선 작업 ...

python3 validate_vault.py > validation_after.txt

diff validation_before.txt validation_after.txt
```

**추적 항목**:
- 고아 페이지 수 감소
- 평균 발견성 점수 증가
- 총 링크 수 증가
- Hub 커버리지 증가

---

## 🚨 문제 해결

### 고아 페이지가 많을 때

```bash
# 1. Agent 실행하여 제안 확인
python3 second_brain_agent.py

# 2. second_brain_report.md에서 link suggestions 확인

# 3. High-confidence 링크 수동 추가
# 또는 자동 적용:
python3 second_brain_agent.py --enhance --apply
```

### Hub 커버리지가 낮을 때

```bash
# 1. Hub suggestions 확인
python3 second_brain_agent.py

# 2. second_brain_report.md에서 hub_suggestions 섹션 확인

# 3. 제안된 Hub 페이지 수동 생성
# 또는 자동 생성:
python3 second_brain_agent.py --enhance --apply
```

### 깨진 링크가 많을 때

```bash
# 1. 검증하여 깨진 링크 목록 확인
python3 validate_vault.py

# 2. vault_validation_report.json 확인

# 3. 수동으로 링크 수정
# - 파일 이름 변경으로 인한 것: 링크 업데이트
# - 삭제된 파일: 링크 제거
```

---

## 🎓 학습 리소스

### Second Brain 철학
- [[Knowledge/Personal/Second-Brain/Concepts/세컨드-브레인-개념]]
- [[Knowledge/Personal/Second-Brain/Concepts/제텔카스텐]]

### Obsidian 활용
- [[Knowledge/Technology/Tools/Obsidian/링크-전략]]
- [[Knowledge/Technology/Tools/Obsidian/메타데이터-관리]]

---

## 📝 체크리스트

### 새 문서 작성 후
- [ ] 메타데이터 완성 (type, category, tags)
- [ ] 최소 200자 이상 내용 작성
- [ ] Related 섹션에 2개 이상 링크
- [ ] 관련 Hub 페이지에 링크 추가

### 주간 유지보수
- [ ] validate_vault.py 실행
- [ ] cleanup_vault.py --apply 실행
- [ ] second_brain_agent.py 실행
- [ ] second_brain_report.md 검토
- [ ] High-confidence 제안 적용

### 월간 최적화
- [ ] 발견성 점수 추세 확인
- [ ] 고아 페이지 수 감소 확인
- [ ] 새 Hub 페이지 필요성 검토
- [ ] 링크 전략 효과 평가

---

## 🔗 관련 문서

- [[KNOWLEDGE_STRUCTURE_DESIGN.md]] - Knowledge 구조 설계
- [[MIGRATION_SUMMARY.md]] - 마이그레이션 요약
- [[RESTRUCTURE_SUMMARY.md]] - 재구조화 요약
- [[README.md]] - 메인 README

---

*Last Updated: 2025-11-28*
*Maintained by: Second Brain Curator Agent*
