# Legacy Import Scripts

이 디렉토리는 Notion import를 위해 작성된 구버전 스크립트들을 보관합니다.

## 📁 파일 목록

### Notion Import 스크립트

#### import_qraft_notion_fixed.py (최종 버전)
- **용도**: Qraft 경험 데이터 Notion → Obsidian 마이그레이션
- **특징**: Child blocks 재귀 처리, 자동 카테고리 분류
- **상태**: ⚠️ 사용 중단, `notion_sync.py`로 대체됨

#### import_qraft_notion.py (구버전)
- **용도**: 초기 버전 import 스크립트
- **상태**: ❌ 더 이상 사용 안 함

#### import_daily_notes.py
- **용도**: Daily Notes import
- **상태**: ⚠️ 참고용

### 파일 관리 스크립트

#### analyze_files.py
- **용도**: vault 파일 분석
- **상태**: 🔧 유틸리티

#### categorize_files.py
- **용도**: 파일 자동 분류
- **상태**: 🔧 유틸리티

#### migrate_files.py
- **용도**: 파일 마이그레이션 헬퍼
- **상태**: 🔧 유틸리티

## 🆕 현재 사용 중인 스크립트

**`automation/notion_sync.py`** (상위 디렉토리)
- mig_status 기반 자동 동기화
- GitHub Actions 통합
- 에러 처리 개선
- Notion 상태 자동 업데이트

## 📚 마이그레이션 히스토리

```
import_qraft_notion.py (v1)
  ↓
import_qraft_notion_fixed.py (v2)
  ↓
notion_sync.py (v3, 현재)
```

### 주요 개선사항

**v1 → v2:**
- Child blocks 재귀 처리 추가
- Markdown 변환 개선
- 카테고리 자동 분류

**v2 → v3 (notion_sync.py):**
- mig_status 필터링 추가
- 환경 변수 지원
- GitHub Actions 통합
- Notion 상태 자동 업데이트 (Done)
- 에러 처리 강화

## ⚠️ 주의사항

- 이 디렉토리의 스크립트들은 **레거시 코드**입니다
- 새 작업에는 `automation/notion_sync.py` 사용
- 참고 및 학습 목적으로만 보관
- 삭제 금지 (히스토리 보존)

## 🔧 실행 방법 (참고용)

### import_qraft_notion_fixed.py
```bash
# 더 이상 권장하지 않음
python automation/legacy/import_qraft_notion_fixed.py
```

### 현재 권장 방법
```bash
# 새로운 동기화 스크립트 사용
python automation/notion_sync.py
```

---

**상태**: 보관용 (Read-only)
**마지막 업데이트**: 2025-11-28
**이동 일자**: 2025-11-28