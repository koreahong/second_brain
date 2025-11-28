# Utility Scripts

Obsidian vault 관리 및 유틸리티 스크립트 모음

## 📁 스크립트 목록

### cleanup_vault.py
**용도**: Vault 정리 및 최적화
- 중복 파일 제거
- 깨진 링크 수정
- 사용하지 않는 파일 정리

**실행**:
```bash
python scripts/cleanup_vault.py
```

### validate_vault.py
**용도**: Vault 무결성 검증
- Frontmatter 검증
- 링크 유효성 확인
- 파일 구조 체크

**실행**:
```bash
python scripts/validate_vault.py
```

### connect_qraft_projects.py
**용도**: Qraft 프로젝트 간 연결 생성
- 프로젝트 백링크 자동 생성
- 관련 노트 연결

**실행**:
```bash
python scripts/connect_qraft_projects.py
```

### second_brain_agent.py
**용도**: Second Brain Agent 관련
- 자동화된 노트 관리
- 지능형 파일 분류

**실행**:
```bash
python scripts/second_brain_agent.py
```

## 🚀 사용법

### 일반 실행
```bash
# 프로젝트 루트에서
python scripts/<script_name>.py
```

### 의존성
대부분의 스크립트는 표준 라이브러리만 사용하지만, 일부는 추가 패키지가 필요할 수 있습니다:
```bash
pip install -r requirements.txt  # 필요시
```

## 🔧 개발 가이드

### 새 스크립트 추가 시
1. 이 디렉토리에 파일 생성
2. 스크립트 상단에 docstring 추가
3. 이 README.md에 설명 추가
4. 실행 예시 포함

### 스크립트 작성 규칙
```python
#!/usr/bin/env python3
"""
스크립트 설명

Usage:
    python scripts/script_name.py [options]
"""

def main():
    # 메인 로직
    pass

if __name__ == '__main__':
    main()
```

## 📝 vs automation/

### scripts/
- **용도**: Vault 관리 유틸리티
- **실행**: 수동, 필요할 때
- **대상**: Vault 파일, 메타데이터
- **예시**: 정리, 검증, 연결 생성

### automation/
- **용도**: Notion ↔ Obsidian 동기화
- **실행**: 자동 (GitHub Actions) 또는 정기적
- **대상**: Notion 데이터
- **예시**: import, sync, migration

## ⚠️ 주의사항

- 스크립트 실행 전 백업 권장
- Git commit 후 실행 (롤백 가능하도록)
- 테스트 환경에서 먼저 검증
- 대량 작업 시 dry-run 모드 사용 (가능한 경우)

## 🔍 문제 해결

### 권한 오류
```bash
chmod +x scripts/<script_name>.py
```

### Python 버전
```bash
python3 --version  # 3.8 이상 권장
```

### 의존성 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

**위치**: `/scripts/`
**타입**: Utility Scripts
**마지막 업데이트**: 2025-11-28