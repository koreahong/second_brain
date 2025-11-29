# 📚 Vault 재구성 가이드

## 🎯 목표

Notion에서 마이그레이션된 콘텐츠를 **PARA + Zettelkasten** 구조로 재구성하여
**프로젝트-지식-경험-결과**가 자동으로 연결되도록 설정

---

## 📊 현재 상태

### 마이그레이션된 데이터베이스 (임시 위치)

| 데이터베이스 | 파일 수 | 내용 | 이동 대상 |
|------------|--------|------|----------|
| 업무리스트 | 46 | 크래프트 업무/프로젝트 | Projects/ |
| 회고록 | 15 | 주간 회고 | Experience/Weekly/ |
| 레퍼런스 | 238 | 기술 지식/개념 | Resources/ |
| 본깨적 | 229 | 인생 인사이트 | Life-Insights/ |

**총 528개 파일** 재구성 대기중

---

## 🏗️ 최종 구조

```
02-Areas/크래프트테크놀로지스/    # 회사 관련
├── Projects/
│   ├── Active/               # 상태: 진행중, 시작
│   ├── Completed/            # 상태: 완료
│   └── Archived/             # 기타
├── Experience/
│   └── Weekly/               # 주간 회고 (회고록)
└── Achievements/             # 성과 기록

03-Resources/                 # 공유 지식 (모든 프로젝트에서 참조)
├── DAE/                      # DAE 역할, 범위
├── Data-Governance/          # Governance, catalog, metadata
├── Technology/               # 기술별 폴더
│   ├── Airflow/
│   ├── DBT/
│   ├── DataHub/
│   ├── Snowflake/
│   └── ...
└── Methodologies/            # Data mesh, medallion 등

30-Flow/Life-Insights/        # 인생 회고 (본깨적)
├── Work/                     # 업무 관련 깨달음
├── Personal/                 # 개인적 경험
└── Observations/             # 일상 관찰
```

---

## 🤖 자동화 설정

### 1. Content Organizer Agent
**파일:** `.claude/agents/content-organizer.md`

Claude Code가 콘텐츠를 자동으로 분류하고 이동

**사용법:**
```
/organize
또는
"organize all migrated content"
```

**분류 규칙:**
- **업무리스트**: `상태` 속성으로 Active/Completed/Archived 분류
- **회고록**: 모두 Experience/Weekly/
- **레퍼런스**: 키워드 분석으로 DAE/Data-Governance/Technology 분류
- **본깨적**: 내용 분석으로 Work/Personal/Observations 분류

### 2. Auto-Organize Hook
**파일:** `.claude/hooks/auto-organize.md`

파일 생성/수정 시 자동 실행되는 Hook

**자동 기능:**
1. 임시 폴더 파일 감지 → 이동 제안
2. 내용 분석 → 자동 태그 추가 (#airflow, #dbt 등)
3. 관련 문서 자동 링크
4. 양방향 백링크 생성

**Frontmatter 설정:**
```yaml
auto_organize: true   # 자동 구성 활성화
auto_tag: true        # 자동 태그
auto_link: true       # 자동 링크
auto_backlink: true   # 자동 백링크
```

### 3. /organize 명령어
**파일:** `.claude/commands/organize.md`

슬래시 명령어로 간편 실행

```
/organize             # content-organizer agent 실행
```

---

## 🔗 자동 연결 전략

### Projects → Knowledge → Experience → Results

각 프로젝트 파일에 자동으로 추가됨:

```markdown
# 프로젝트 제목

## Related Knowledge
- [[03-Resources/Technology/Airflow/DAG-Patterns]]
- [[03-Resources/Data-Governance/Metadata-Management]]

## Weekly Reflections
- [[Experience/Weekly/2025년-11월-24일]]

## Insights
- [[Life-Insights/Work/datahub-론칭-배운점]]

## Results
- 성과: DataHub 도입으로 메타데이터 관리 30% 개선
- 개선율: 데이터 검색 시간 50% 단축
```

---

## 📝 사용 시나리오

### Scenario 1: 전체 재구성
```
사용자: "organize all migrated content"

Claude:
1. 업무리스트 46개 분석 → Projects/로 분류
2. 회고록 15개 이동 → Experience/Weekly/
3. 레퍼런스 238개 분류 → Resources/ (주제별)
4. 본깨적 229개 분류 → Life-Insights/ (컨텍스트별)
5. 자동 태그 추가
6. 관련 문서 링크 생성
```

### Scenario 2: 개별 데이터베이스 재구성
```
사용자: "organize 업무리스트"

Claude:
- 46개 파일의 '상태' 확인
- Active/Completed/Archived로 분류
- 관련 기술 키워드 추출 → Resources/ 링크
- 주차 정보로 회고록 연결
```

### Scenario 3: 새 파일 작성 시 자동 처리
```
사용자: (Projects/Active/에 새 파일 작성)

Claude (Hook 자동 실행):
1. 내용에서 "airflow" 발견 → #airflow 태그 추가
2. Airflow 관련 Resources/ 검색 → 자동 링크
3. 해당 주차 회고록 링크
```

---

## ⚙️ 세부 설정

### Frontmatter 자동 추가

재구성된 모든 파일에 추가됨:
```yaml
reorganized: 2025-11-29
original_database: 업무리스트
vault_location: Projects
related_projects: []
related_knowledge: []
auto_organize: true
auto_tag: true
auto_link: true
```

### 기술별 자동 분류 키워드

**Data Governance:**
- governance, catalog, lineage, datahub, metadata, quality, openmetadata

**Technology:**
- airflow, dbt, snowflake, docker, kafka, iceberg, trino, jenkins, kubernetes

**DAE:**
- dae, 역할, scope, responsibilities

**Methodologies:**
- mesh, medallion, lakehouse, methodology, framework

---

## 🚀 시작하기

1. **현재 상태 확인**
   ```
   ls -la 업무리스트/ 회고록/ 레퍼런스/ 본깨적/
   ```

2. **재구성 시작**
   ```
   /organize
   또는
   "organize all migrated content"
   ```

3. **결과 확인**
   ```
   02-Areas/크래프트테크놀로지스/Projects/
   03-Resources/Technology/
   30-Flow/Life-Insights/
   ```

4. **자동 링크 확인**
   - 아무 프로젝트 파일 열기
   - "Related Knowledge" 섹션 확인
   - "Weekly Reflections" 섹션 확인

---

## 📌 주의사항

1. **백업**: 재구성 전 Git commit 권장
2. **확인**: 대량 이동 시 사용자 승인 필요
3. **보존**: 원본 frontmatter 모두 유지
4. **MCP Only**: Obsidian MCP 도구만 사용 (Python/Bash 금지)

---

**마지막 업데이트**: 2025-11-29
**작성자**: Claude Code (Sonnet 4.5)
