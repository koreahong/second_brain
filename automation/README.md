---
tags:
  - automation
  - index
created: '2025-11-28'
type: index
---
# Automation

이 디렉토리에는 vault 자동화 관련 스크립트와 문서가 포함되어 있습니다.

## 📚 문서

- [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) - Notion to Obsidian 자동화 전체 설정 가이드

## 🔧 스크립트

### notion_sync.py

Notion에서 `mig_status=NEEDED`인 페이지를 자동으로 Obsidian vault로 동기화합니다.

**사용법**:
```bash
# 기본 실행 (work_list 데이터베이스)
python automation/notion_sync.py

# 특정 데이터베이스 지정
TARGET_DB=dae_work python automation/notion_sync.py

# 모든 항목 강제 동기화
FORCE_SYNC=true python automation/notion_sync.py
```

**주요 기능**:
- mig_status 필터링
- 재귀적 child blocks 처리
- 자동 카테고리 분류
- Notion 상태 자동 업데이트

## 🤖 GitHub Actions

`.github/workflows/notion-sync.yml` - 매일 자동 실행되는 워크플로우

**스케줄**: 매일 한국 시간 오전 9시 (UTC 0시)

**수동 실행**: GitHub Actions 탭에서 가능

## 🔐 설정 파일

- `config.json` - 실제 설정 (gitignore됨, 절대 커밋 금지)
- `config.template.json` - 설정 템플릿

## 📖 빠른 시작

1. [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) 읽기
2. Notion API Token 발급
3. GitHub Secrets 설정
4. 테스트 실행

---

상세한 내용은 [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md)를 참조하세요.
