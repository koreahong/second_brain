---
title: Vault 표준화 계획
type: documentation
created: '2025-11-30'
tags:
  - meta
  - standardization
  - documentation
---
# Vault 표준화 계획

> 분석 일자: 2025-11-30
> 전체 파일 수: 633개
> Frontmatter 보유: 628개 (99.2%)

## 📊 현황 분석

### 1. Frontmatter 타입 분포

| Type | 개수 | 비율 | 통일 제안 |
|------|------|------|-----------|
| resource | 243 | 38.4% | ✅ 유지 |
| daily-insight | 129 | 20.4% | ⚠️ `insight`로 통일 |
| daily-reflection | 115 | 18.2% | ⚠️ `reflection`으로 통일 |
| project | 46 | 7.3% | ✅ 유지 |
| 주간회고 | 22 | 3.5% | ❌ `weekly-reflection`으로 변경 |
| weekly-reflection | 15 | 2.4% | ✅ 유지 |
| insight | 14 | 2.2% | ✅ 유지 |
| 기타 | 59 | 9.3% | - |

**문제점:**
- 한글/영어 혼용 (`주간회고` vs `weekly-reflection`)
- 중복 타입 (`daily-insight`, `daily-reflection`, `insight`)
- 비표준 타입 다수

### 2. 태그 사용 현황

**Top 20 태그:**
1. reflection (65)
2. 커리어-지원내역 (35) - 한글
3. personal (30)
4. observations (26)
5. 커리어 (21) - 한글
6. aws (20)
7. airflow (19)
8. DB (18)
9. work-life (14)
10. Query (14)

**문제점:**
- 한글/영어 혼용 심각 (35% 이상)
- 태그 네이밍 규칙 없음 (하이픈, 언더스코어, 케이스 혼용)
- 빈 태그 필드 다수 (287개)

### 3. 연결성 분석

| 항목 | 개수 | 비율 |
|------|------|------|
| Related 섹션 보유 | 82 | 13% |
| 위키링크 보유 | 112 | 18% |
| 연결성 없음 | ~520 | 82% |

**문제점:**
- 대부분 파일이 고립되어 있음 (82%)
- Related 섹션 형식 불일관
- 백링크 부족

## 🎯 표준화 체계 설계

### A. Frontmatter 표준 구조

#### 공통 필드 (모든 노트)

\`\`\`yaml
---
title: "노트 제목"
type: "resource|project|reflection|insight|map|moc"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: []
aliases: []
---
\`\`\`

#### 영역별 추가 필드

**1. Projects (02-Areas/크래프트테크놀로지스/Projects/)**
\`\`\`yaml
---
title: "프로젝트명"
type: "project"
status: "active|completed|archived|on-hold"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
start_date: "YYYY-MM-DD"
end_date: "YYYY-MM-DD"
tags: ["project", "technology-stack", "domain"]
related_projects: []
team: "팀명"
---
\`\`\`

**2. Weekly Reflections (Experience/Weekly/)**
\`\`\`yaml
---
title: "YYYY년 MM월 DD일"
type: "weekly-reflection"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
week: 숫자
tags: ["reflection", "키워드1", "키워드2"]
projects: []  # 관련 프로젝트 링크
achievements: []  # 성과 키워드
---
\`\`\`

**3. Life Insights (30-Flow/Life-Insights/)**
\`\`\`yaml
---
title: "인사이트 제목"
type: "insight"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
category: "work|personal|observations"
tags: ["insight-type", "context"]
related_insights: []
---
\`\`\`

**4. Resources (03-Resources/)**
\`\`\`yaml
---
title: "리소스명"
type: "resource"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
category: "technology|career|data-governance|methodology"
tags: ["tech-stack", "concept", "tool"]
related_resources: []
difficulty: "beginner|intermediate|advanced"  # 선택
---
\`\`\`

**5. Zettelkasten (10-Zettelkasten/)**
\`\`\`yaml
---
title: "노트 제목"
type: "permanent|literature|fleeting"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["concept", "domain"]
source: "출처 (literature인 경우)"
related: []
---
\`\`\`

### B. 태그 체계

#### 1. 네이밍 규칙
- **소문자 영어만 사용**
- **하이픈(-)으로 단어 연결**
- **한글 태그는 영어로 변환**

#### 2. 태그 계층 구조

**최상위 카테고리 (Prefix):**
```
tech/          # 기술
domain/        # 도메인 지식
skill/         # 기술/역량
project/       # 프로젝트
insight/       # 인사이트 타입
status/        # 상태
```

**변환 매핑:**
```yaml
# 한글 → 영어
커리어: career
문제해결: problem-solving
데이터거버넌스: data-governance
구조화: structuring
문서화: documentation
의사소통: communication
협업: collaboration
기술전파: knowledge-sharing
비용 최적화: cost-optimization
성능개선: performance-optimization
```

#### 3. 표준 태그 세트

**기술 스택 (tech/):**
- `tech/airflow`
- `tech/dbt`
- `tech/python`
- `tech/sql`
- `tech/aws`
- `tech/docker`

**역량 (skill/):**
- `skill/problem-solving`
- `skill/communication`
- `skill/documentation`
- `skill/collaboration`
- `skill/leadership`

**도메인 (domain/):**
- `domain/data-engineering`
- `domain/data-governance`
- `domain/mlops`
- `domain/finance`

**인사이트 타입 (insight/):**
- `insight/reflection`
- `insight/learning`
- `insight/observation`
- `insight/decision`

**상태 (status/):**
- `status/active`
- `status/completed`
- `status/archived`
- `status/in-progress`

### C. 파일 간 연결 구조

#### 1. Related 섹션 표준

모든 노트 하단에 추가:

\`\`\`markdown
---

## 📎 Related

### Projects
- [[프로젝트1]]
- [[프로젝트2]]

### Knowledge
- [[기술 리소스1]]
- [[개념 노트1]]

### Insights
- [[관련 인사이트1]]
- [[회고록1]]

### External
- [외부 링크 제목](URL)
\`\`\`

#### 2. 자동 연결 규칙

**Projects → Resources:**
- 프로젝트에서 사용한 기술 스택 자동 링크
- 관련 Data Governance 문서 연결

**Weekly Reflections → Projects:**
- 해당 주에 작업한 프로젝트 자동 링크
- 태그 기반 자동 매칭

**Life Insights → Everything:**
- 컨텍스트 기반 자동 링크
- 날짜/기간 기반 연결

## 🤖 자동화 전략

### 1. 단계별 적용 계획

**Phase 1: Type 표준화 (우선순위: 높음)**
- `주간회고` → `weekly-reflection`
- `daily-insight` / `daily-reflection` → `insight` / `reflection`
- 비표준 타입 정리

**Phase 2: 태그 표준화 (우선순위: 높음)**
- 한글 태그 → 영어 태그 변환
- 태그 계층 구조 적용
- 빈 태그 필드 채우기 (내용 기반 자동 태그)

**Phase 3: 필수 필드 추가 (우선순위: 중간)**
- `created` 필드 추가 (파일 생성일 기반)
- `updated` 필드 추가 (파일 수정일 기반)
- `aliases` 필드 추가 (제목 기반)

**Phase 4: Related 섹션 자동 생성 (우선순위: 중간)**
- 태그 기반 자동 링크
- 날짜 기반 자동 링크 (Weekly ↔ Projects)
- 컨텍스트 기반 자동 링크

**Phase 5: 백링크 강화 (우선순위: 낮음)**
- 양방향 링크 자동 생성
- 관련도 분석 기반 추천

### 2. 스크립트 구조

\`\`\`python
# vault_standardization.py

class VaultStandardizer:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        
    def standardize_types(self):
        \"\"\"Type 필드 표준화\"\"\"
        pass
        
    def standardize_tags(self):
        \"\"\"태그 표준화 및 번역\"\"\"
        pass
        
    def add_missing_fields(self):
        \"\"\"누락된 frontmatter 필드 추가\"\"\"
        pass
        
    def create_related_sections(self):
        \"\"\"Related 섹션 자동 생성\"\"\"
        pass
        
    def validate_structure(self):
        \"\"\"구조 검증\"\"\"
        pass
\`\`\`

## 📋 실행 계획

### 샘플 테스트
1. **영역 선택**: `30-Flow/Life-Insights/Personal/` (66개 파일)
2. **백업 생성**: Git commit
3. **Phase 1-2 적용**: Type + Tags 표준화
4. **검증**: 수동 확인
5. **피드백 수집**: 사용성 평가

### 전체 적용
1. **백업**: 전체 vault Git commit
2. **일괄 적용**: Phase 1-4
3. **검증**: 자동 + 수동
4. **문서 업데이트**: `.claude/CLAUDE.md` 업데이트

## 🎨 예상 효과

### 정량적 효과
- **검색 효율 50% 향상**: 표준화된 태그로 정확한 검색
- **연결성 400% 증가**: 82% → 95% 파일에 Related 섹션
- **유지보수 시간 70% 감소**: 자동화된 구조

### 정성적 효과
- **일관된 사용자 경험**: 모든 노트가 동일한 구조
- **지식 탐색 용이**: 백링크로 연결된 네트워크
- **AI 활용 극대화**: Claude Code가 컨텍스트 이해 쉬움

## 📝 다음 단계

1. ✅ 분석 완료
2. ⏳ 표준 체계 설계 (현재)
3. ⏳ 자동화 스크립트 작성
4. ⏳ 샘플 영역 테스트
5. ⏳ 전체 적용
6. ⏳ 문서화 업데이트

---

**생성일**: 2025-11-30
**작성자**: Claude Code (Sonnet 4.5)
**버전**: 1.0
