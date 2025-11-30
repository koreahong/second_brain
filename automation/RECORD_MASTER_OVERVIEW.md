# 레코드 마스터 시스템 개요

## 🎯 핵심 개념

**하나의 Notion 데이터베이스로 모든 것을 관리**

```
┌─────────────────────────────────────────────┐
│         Notion 레코드 마스터 DB             │
│                                             │
│  - 업무 (Projects)                          │
│  - 회고 (Experiences)                       │
│  - 기술 문서 (References)                   │
│  - 인사이트 (Insights)                      │
│  - 외부 기사 (Articles)                     │
│  - 독서 노트 (Books)                        │
│                                             │
│  속성:                                      │
│  ├─ Content_Type (무엇인가?)                │
│  ├─ Source (어디서 왔는가?)                 │
│  ├─ Mig_Status (마이그레이션 상태)          │
│  ├─ Mig_Priority (우선순위)                 │
│  └─ Tags, Category, Company, Period...     │
└─────────────────────────────────────────────┘
                    ↓
            Mig_Status = NEEDED
                    ↓
┌─────────────────────────────────────────────┐
│         GitHub Actions (자동화)             │
│                                             │
│  1. Notion API로 NEEDED 레코드 가져오기     │
│  2. Content_Type별 분류                     │
│  3. Obsidian vault에 파일 생성              │
│  4. Mig_Status → DONE 업데이트              │
│  5. Obsidian_Path 기록                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Obsidian Vault (결과)               │
│                                             │
│  02-Areas/.../Projects/                     │
│  02-Areas/.../Experience/Weekly/            │
│  03-Resources/Technology/                   │
│  30-Flow/Life-Insights/                     │
│  03-Resources/Articles/                     │
│  03-Resources/Books/                        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       Auto-Organize Hook (최적화)           │
│                                             │
│  1. 콘텐츠 분석                             │
│  2. 적절한 위치로 이동 제안                 │
│  3. 관련 노트 자동 연결                     │
│  4. 태그 정규화                             │
│  5. 백링크 생성                             │
└─────────────────────────────────────────────┘
```

## 📋 주요 구성 요소

### 1. Notion 레코드 마스터 데이터베이스

**위치**: https://www.notion.so/2bbc6d433b4d803e8f1cdc23bda7b7c7

**역할**:
- 모든 콘텐츠의 단일 진실 공급원 (Single Source of Truth)
- 마이그레이션 상태 추적
- 콘텐츠 분류 및 메타데이터 관리

**핵심 속성**:
| 속성 | 용도 |
|------|------|
| Content_Type | Project, Experience, Reference, Insight, Article, Book |
| Mig_Status | NEEDED, IN_PROGRESS, DONE, SKIP, ERROR |
| Mig_Priority | High, Medium, Low |
| Source | 업무리스트, 회고록, 레퍼런스, 본깨적, 외부 등 |
| Obsidian_Path | 마이그레이션된 파일 경로 |

### 2. notion_sync.py

**위치**: `automation/notion_sync.py`

**역할**:
- Notion API로 NEEDED 레코드 조회
- Content_Type별 자동 분류
- Obsidian 노트 생성 (frontmatter 포함)
- Notion 상태 업데이트

**핵심 함수**:
```python
RecordMasterSync
├── fetch_records_to_migrate()    # NEEDED 레코드 조회
├── extract_page_properties()     # 속성 추출
├── get_page_content()            # 본문 가져오기
├── determine_target_path()       # 목표 경로 결정
├── create_obsidian_note()        # 노트 생성
└── update_migration_status()     # 상태 업데이트
```

### 3. GitHub Actions 워크플로우

**위치**: `.github/workflows/notion-sync-master.yml`

**스케줄**: 매일 00:00 UTC (한국 시간 09:00)

**프로세스**:
1. Repository checkout
2. Python 환경 설정
3. config.json 생성 (Secrets 사용)
4. notion_sync.py 실행
5. Git commit & push

### 4. Obsidian Auto-Organize Hook

**위치**: `.claude/hooks/auto-organize.md`

**트리거**: 파일 생성/수정 시

**기능**:
- 위치 최적화 제안
- 관련 노트 자동 연결
- 태그 정규화
- 백링크 생성

## 🔄 전체 플로우

### Phase 1: Notion에서 콘텐츠 작성

```
1. 레코드 마스터 DB 열기
2. 템플릿 선택:
   - 📁 New Project
   - 📝 New Experience
   - 📚 New Reference
   - 💡 New Insight
   - 📰 New Article
   - 📖 New Book
3. 내용 작성
4. 속성 설정:
   ✅ Content_Type (자동)
   ✅ Mig_Status = NEEDED (자동)
   ✅ Mig_Priority 선택
   ✅ Tags 추가
   ✅ Company, Period 등
5. 저장
```

### Phase 2: 자동 마이그레이션

```
# 로컬 테스트
cd automation
python notion_sync.py

# 또는 GitHub Actions (매일 자동)
GitHub → Actions → Notion Record Master Sync
```

**처리 과정**:
```
1. Notion API 호출
   ├─ Filter: Mig_Status = NEEDED
   ├─ Sort: Mig_Priority (High → Low)
   └─ Limit: 50건/배치

2. Content_Type별 분류
   ├─ Project → 02-Areas/.../Projects/Active/
   ├─ Experience → 02-Areas/.../Experience/Weekly/
   ├─ Reference → 03-Resources/[Category]/
   ├─ Insight → 30-Flow/Life-Insights/[Work|Personal]/
   ├─ Article → 03-Resources/Articles/
   └─ Book → 03-Resources/Books/

3. Obsidian 노트 생성
   ├─ Frontmatter 생성
   ├─ 본문 변환 (Markdown)
   └─ 파일 저장

4. Notion 상태 업데이트
   ├─ Mig_Status → DONE
   ├─ Mig_Date → 현재 시각
   └─ Obsidian_Path → 파일 경로
```

### Phase 3: 재분류 및 최적화

```
Auto-Organize Hook 자동 실행:

1. 콘텐츠 분석
   ├─ frontmatter 읽기
   ├─ 현재 위치 확인
   └─ 권장 위치 계산

2. 관련 노트 찾기
   ├─ 같은 시기 Weekly 회고
   ├─ 관련 Projects
   ├─ 유사한 Reference
   └─ 연결된 Insights

3. 연결 생성
   ├─ 양방향 백링크
   ├─ 맥락 설명 추가
   └─ 섹션별 정리

4. 최적화
   ├─ 태그 정규화
   ├─ 중복 제거
   └─ 응집도 향상
```

## 📊 통계 및 모니터링

### Notion 대시보드

**View 1: 🚀 마이그레이션 대기**
```sql
Filter: Mig_Status = NEEDED
Group: Content_Type
Sort: Mig_Priority

현황:
  High: 23건
  Medium: 87건
  Low: 142건
  ────────────
  Total: 252건
```

**View 2: ✅ 완료**
```sql
Filter: Mig_Status = DONE
Sort: Mig_Date (최신순)

통계:
  이번 주: 45건
  이번 달: 198건
  전체: 276건
```

**View 3: 📊 타입별**
```sql
Group: Content_Type

분포:
  Project: 46건 (16%)
  Experience: 15건 (5%)
  Reference: 238건 (84%)
  Insight: 229건 (81%)
  Article: 52건 (18%)
  Book: 18건 (6%)
```

### GitHub Actions 로그

```
✨ Migration complete!
   ✅ Success: 23
   ❌ Errors: 0

📝 Processing: 테스트 회고
   ✅ Created: 02-Areas/.../Weekly/테스트-회고.md

📝 Processing: Airflow 3.0 학습
   ✅ Created: 03-Resources/Technology/Airflow/Airflow-3.0-학습.md

...
```

## 🎯 사용 시나리오

### 시나리오 1: 주간 회고 작성

```
1. Notion 레코드 마스터 열기
2. "📝 New Experience" 템플릿 클릭
3. 회고 작성:
   - 제목: "2025년 12월 1일"
   - Content_Type: Experience (자동)
   - Mig_Status: NEEDED (자동)
   - Mig_Priority: High
   - Company: Qraft
   - Period: 2025-12-01
   - 본문: 이번 주 작업, 배운 점, 개선점
4. 저장

→ GitHub Actions 실행 (다음날 09시)
→ Obsidian에 자동 생성: 02-Areas/.../Weekly/2025년-12월-1일.md
→ Auto-Organize Hook:
   - 같은 주 프로젝트 자동 연결
   - 관련 인사이트 연결
   - 태그 정규화
```

### 시나리오 2: 기술 문서 추가

```
1. "📚 New Reference" 템플릿 클릭
2. 문서 작성:
   - 제목: "DBT Incremental Models"
   - Content_Type: Reference (자동)
   - Category: Technology
   - Tags: #DBT, #DataEngineering
   - Mig_Priority: Medium
   - 본문: 개념, 사용법, 예제
3. 저장

→ 마이그레이션
→ Obsidian: 03-Resources/Technology/DBT/DBT-Incremental-Models.md
→ 관련 프로젝트에 자동 백링크
```

### 시나리오 3: 인사이트 기록

```
1. "💡 New Insight" 템플릿 클릭
2. 인사이트 작성:
   - 제목: "데이터 거버넌스의 중요성"
   - Content_Type: Insight (자동)
   - Company: Qraft
   - Period: 2025-10-29
   - Tags: #인사이트, #거버넌스
   - Mig_Priority: High
   - 본문: 배경, 깨달은 점, 적용 방안
3. 저장

→ 마이그레이션
→ Obsidian: 30-Flow/Life-Insights/Work/데이터-거버넌스의-중요성.md
→ 관련 프로젝트 및 회고 자동 연결
```

## 🔧 설정 파일

### config.json

```json
{
  "notion": {
    "api_token": "secret_xxxxx",
    "record_master_db_id": "2bbc6d433b4d803e8f1cdc23bda7b7c7",
    "sync_settings": {
      "filter_status": "NEEDED",
      "batch_size": 50,
      "priority_order": ["High", "Medium", "Low"]
    }
  },
  "obsidian": {
    "vault_path": "/Users/.../Second-Brain",
    "location_mapping": {
      "Project": "02-Areas/.../Projects/Active",
      "Experience": "02-Areas/.../Experience/Weekly",
      "Reference": "03-Resources",
      "Insight": "30-Flow/Life-Insights",
      "Article": "03-Resources/Articles",
      "Book": "03-Resources/Books"
    }
  }
}
```

### GitHub Secrets

```
NOTION_API_TOKEN: secret_xxxxxxxxxxxxx
RECORD_MASTER_DB_ID: 2bbc6d433b4d803e8f1cdc23bda7b7c7
```

## 📚 문서 구조

```
automation/
├── README.md                     # 메인 README (이 시스템 소개)
│
├── RECORD_MASTER_OVERVIEW.md     # ⭐ 이 파일 (전체 개요)
├── QUICK_START_MASTER.md         # 빠른 시작 (5분)
├── RECORD_MASTER_SCHEMA.md       # DB 스키마 상세
├── AUTOMATION_MASTER_SYNC.md     # 코드 상세 가이드
└── NOTION_TEMPLATES.md           # 6가지 템플릿
```

**읽는 순서**:
1. **이 파일** (RECORD_MASTER_OVERVIEW.md) - 전체 이해
2. [QUICK_START_MASTER.md](QUICK_START_MASTER.md) - 실제 설정 및 실행
3. [RECORD_MASTER_SCHEMA.md](RECORD_MASTER_SCHEMA.md) - DB 구조 상세
4. [AUTOMATION_MASTER_SYNC.md](AUTOMATION_MASTER_SYNC.md) - 코드 커스터마이징
5. [NOTION_TEMPLATES.md](NOTION_TEMPLATES.md) - 템플릿 활용

## 🎉 장점

### vs 기존 방식 (4개 개별 DB)

| 구분 | 기존 | 레코드 마스터 |
|------|------|--------------|
| 관리 포인트 | 4개 DB | 1개 DB |
| 태그 일관성 | 낮음 | 높음 |
| 검색 편의성 | 분산됨 | 통합됨 |
| 마이그레이션 추적 | 어려움 | 쉬움 |
| 우선순위 관리 | 없음 | 있음 |
| 템플릿 | 없음 | 6종 제공 |
| 통계/대시보드 | 분산 | 통합 |

### 핵심 이점

1. **단순성**: 하나의 DB만 관리
2. **일관성**: 표준 템플릿 사용
3. **가시성**: 통합 대시보드
4. **추적성**: Mig_Status로 상태 관리
5. **우선순위**: High/Medium/Low 지정
6. **확장성**: 새 콘텐츠 타입 쉽게 추가

## 🚀 다음 단계

1. ✅ [QUICK_START_MASTER.md](QUICK_START_MASTER.md) 읽기
2. ✅ Notion 레코드 마스터 DB 생성
3. ✅ 템플릿 6종 추가
4. ✅ Integration 설정
5. ✅ 테스트 레코드 마이그레이션
6. ⬜ 기존 데이터 일괄 분류
7. ⬜ 우선순위별 마이그레이션
8. ⬜ Auto-Organize Hook 활성화
9. ⬜ 품질 검증 및 최적화

---

**버전**: 1.0
**작성일**: 2025-11-30
**작성자**: Claude Code

**질문/피드백**: automation/.claude/AUTOMATION_AGENT.md 참고
