---
created: 2025-11-28
tags: [meta, restructure, plan]
---

# Vault 전체 재구성 계획

## 🎯 목표

1. **명확한 구조**: PARA 기반 + 번호 prefix로 우선순위 명확화
2. **중복 제거**: Notion Import 데이터 통합
3. **표준화**: Frontmatter, 태그, 네이밍 통일

## 📊 현재 상황

**총 347개 파일 (Notion Import 제외)**

- Career: 67개
- Work (Qraft): 52개  
- Learning (Knowledge): 109개
- Projects: 14개
- Daily/Weekly: 17개
- Concepts (Atoms): 39개
- Other: 49개

## 🏗️ 새로운 구조

```
DAE-Second-Brain/
│
├── 00-System/              # 메타, 설정, 템플릿 (10개)
│   ├── Templates/
│   ├── Indexes/
│   └── Configs/
│
├── 10-Inbox/               # 임시 노트, 처리 대기
│
├── 20-Areas/               # 지속적 관심 영역 (67개)
│   ├── Career/
│   │   ├── Job-Search/    # Applications + Interview 통합
│   │   ├── Skills/
│   │   └── Goals/
│   └── Personal/
│
├── 30-Projects/            # 현재 진행 프로젝트 (14개)
│   ├── Active/
│   └── Completed/
│
├── 40-Work/                # 업무 경험 (99개)
│   └── Qraft/
│       ├── Projects/      # 46개 프로젝트
│       ├── Work-Items/    # 46개 업무리스트 (Notion)
│       ├── Planning/      # 30개 업무 구상 (Notion)
│       └── Retrospectives/ # 17개 회고 (Notion)
│
├── 50-Knowledge/           # 학습 자료 (228개)
│   ├── Technology/        # 109개 기술 문서
│   ├── Concepts/          # 39개 개념 (Atoms)
│   ├── References/        # 100개 레퍼런스 (Notion)
│   └── Fundamentals/      # 19개 펀더멘탈 (Notion)
│
├── 60-Flow/                # 시간 기반 노트 (17개)
│   ├── Daily/
│   └── Weekly/
│
└── 90-Archives/            # 완료/보관
    └── Old-Notion-Import/
```

## 🔄 마이그레이션 매핑

### Career (67개)
```
Areas/Career/Applications/  (45)  →  20-Areas/Career/Job-Search/Applications/
Areas/Career/Interview/     (20)  →  20-Areas/Career/Job-Search/Interview/
Areas/Career/Learning-Path/ (1)   →  20-Areas/Career/Skills/
Notion Import/지원.md             →  DELETE (데이터 이미 통합됨)
Notion Import/면접준비.md         →  20-Areas/Career/Job-Search/_Index.md
```

### Work (99개)
```
Experiences/Qraft/Projects/       (46)  →  40-Work/Qraft/Projects/
Notion Import/업무리스트.md       (46)  →  40-Work/Qraft/Work-Items/ (개별 파일로)
Notion Import/업무_구상.md        (30)  →  40-Work/Qraft/Planning/ (개별 파일로)
Notion Import/크래프트_회고.md    (17)  →  40-Work/Qraft/Retrospectives/
```

### Knowledge (228개)
```
Knowledge/                       (109)  →  50-Knowledge/Technology/
Atoms/Concepts/                  (13)   →  50-Knowledge/Concepts/
Atoms/Problems/                  (26)   →  50-Knowledge/Concepts/Problems/
Notion Import/레퍼런스.md        (100)  →  50-Knowledge/References/ (개별 파일로)
Notion Import/펀더멘탈.md        (19)   →  50-Knowledge/Fundamentals/
Notion Import/세컨드_브레인.md   (6)    →  분산 배치
```

### Projects (14개)
```
Projects/Staging/                (14)   →  30-Projects/Active/
Projects/Active/                        →  30-Projects/Active/
```

### Flow (17개)
```
Flow/Daily/                            →  60-Flow/Daily/
Flow/Weekly/                    (16)   →  60-Flow/Weekly/
```

### System
```
Templates/                      (10)   →  00-System/Templates/
automation/                     (4)    →  00-System/Automation/
.claude/                               →  00-System/Claude/
```

## 📝 표준화 규칙

### Frontmatter Schema
```yaml
---
title: 제목
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
aliases: []
type: [note|project|concept|reference]
status: [active|completed|archived]
---
```

### 네이밍 컨벤션
- 폴더: PascalCase with hyphens (Job-Search, Work-Items)
- 파일: 의미있는 제목, 언더스코어 허용
- 번호 prefix: 00-90 (우선순위/순서)

### 태그 체계
- `#career` - 커리어 관련
- `#work/qraft` - Qraft 업무
- `#tech/{technology}` - 기술 문서
- `#concept` - 개념 노트
- `#reference` - 참고 자료
- `#daily` / `#weekly` - 시간 기반

## ⚠️ 주의사항

1. **백업 필수**: 재구성 전 전체 백업
2. **단계적 진행**: 한 번에 한 카테고리씩
3. **검증**: 각 단계 후 링크 확인

## 🚀 실행 순서

1. ✅ 구조 설계 완료
2. [ ] 새 폴더 구조 생성
3. [ ] System 파일 이동
4. [ ] Career 파일 이동 및 통합
5. [ ] Work 파일 이동 및 Notion 통합
6. [ ] Knowledge 파일 이동 및 Notion 통합
7. [ ] Projects & Flow 이동
8. [ ] 전체 Frontmatter 표준화
9. [ ] 태그 통일
10. [ ] 인덱스 생성
11. [ ] 구 Notion Import 폴더 아카이브
12. [ ] 최종 검증

