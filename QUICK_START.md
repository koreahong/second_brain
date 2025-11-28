# 🚀 Quick Start Guide

## 1분 안에 시작하기

### Step 1: Obsidian 설치
```bash
# macOS
brew install --cask obsidian

# 또는 https://obsidian.md 에서 다운로드
```

### Step 2: Vault 열기
1. Obsidian 실행
2. "Open folder as vault" 선택
3. `~/DAE-Second-Brain` 폴더 선택

### Step 3: 플러그인 설치 (Community Plugins)
1. Settings (⚙️) → Community plugins
2. "Turn on community plugins" 클릭
3. Browse → 다음 플러그인 설치:
   - **Dataview** ⭐⭐⭐
   - **Templater** ⭐⭐⭐
   - **Calendar** ⭐⭐
   - **Obsidian Git** ⭐⭐

### Step 4: 첫 Daily Note 생성
- `Cmd + T` 또는
- 왼쪽 달력 아이콘 클릭

## 📝 일일 워크플로우

### 아침 (9:00)
```
1. Cmd + T → Daily Note 생성
2. 오늘 목표 3가지 작성
3. 관련 프로젝트 링크 [[프로젝트명]]
```

### 작업 중
```
문제 발생 →
1. Cmd + N → 새 노트
2. 0-Inbox/문제-제목.md 로 저장
3. Templates/problem-solving 적용
4. 즉시 시행착오 기록!
```

### 저녁 (18:00)
```
1. Daily Note에 회고 작성
2. Inbox 정리 (0-Inbox → 적절한 폴더로 이동)
3. Git 커밋 활동 자동 추가:
   cd ~/qraft_data_platform
   ./.dae/obsidian_sync.py
```

### 금요일
```
1. 이번 주 Daily Notes 리뷰
2. 완료된 프로젝트 → 4-Archives로 이동
3. Graph View (Cmd + G)로 이번 주 지식 연결 확인
```

## 🎯 핵심 단축키

| 기능 | 단축키 |
|------|--------|
| Quick Switcher | `Cmd + O` |
| 전체 검색 | `Cmd + Shift + F` |
| Graph View | `Cmd + G` |
| Daily Note | `Cmd + T` |
| 새 노트 | `Cmd + N` |
| 명령 팔레트 | `Cmd + P` |

## 📊 자동화

### Git → Obsidian 동기화
```bash
# 오늘의 커밋을 Daily Note에 자동 추가
cd ~/qraft_data_platform
./.dae/obsidian_sync.py
```

### Git 자동 백업 (Obsidian Git 플러그인)
```
Settings → Obsidian Git
- Vault backup interval: 30분
- Auto pull interval: 10분
```

## 🔍 검색 팁

### 1. Quick Switcher (`Cmd + O`)
```
metadata      → Metadata-Management.md 찾기
2025-11-27    → 특정 날짜 Daily Note 찾기
MPD-75        → 프로젝트 찾기
```

### 2. Global Search (`Cmd + Shift + F`)
```
"Snowflake RBAC"   → 정확한 구문 검색
tag:#learning      → 태그로 검색
path:Learning/     → 특정 폴더에서 검색
```

### 3. Dataview 쿼리
```dataview
TABLE 문제, 해결방법
FROM "Learning/Problems"
WHERE contains(tags, "Snowflake")
SORT 날짜 DESC
```

## 🧩 템플릿 사용법

### Daily Note (자동)
- `Cmd + T` 누르면 자동으로 템플릿 적용

### Project
```
1. Cmd + N
2. 1-Projects/프로젝트명.md
3. Cmd + P → "Insert template"
4. "project" 선택
```

### Learning
```
1. Cmd + N
2. Learning/Concepts/개념명.md
3. Templates/learning 적용
```

## 🌐 Graph View 활용

### 전체 Graph
```
Cmd + G → 전체 지식 네트워크 시각화
```

### 필터링
```
# 진행 중인 프로젝트만
tag:#project AND tag:#진행중

# 특정 영역만
path:2-Areas/Data-Governance

# 최근 7일
file.mtime > date(today) - dur(7 days)
```

## 💡 Best Practices

### 1. 원자적 노트 작성
```markdown
# ❌ 나쁜 예
DataHub 전체 설정 및 OIDC 통합 및 Policy 관리.md

# ✅ 좋은 예
DataHub-OIDC-Redirect-URI-설정.md
Keycloak-Client-Scope-설정.md
DataHub-Policy-우선순위-이해.md
```

### 2. 링크 많이 추가
```markdown
# 모든 노트는 최소 3개 이상 링크!

관련 개념: [[OIDC]] [[JWT]]
관련 프로젝트: [[DataHub-OIDC]]
관련 문제: [[Redirect-URI-오류]]
```

### 3. 태그 일관성
```markdown
# 일관된 태그 사용
#DataHub #인증 #OIDC #완료

# 태그 계층
#DataHub/설정
#DataHub/문제해결
```

### 4. Inbox 정리
```
매일 저녁 0-Inbox 비우기!
→ 적절한 폴더로 분류
```

## 🔄 백업

### Git 백업 (권장)
```bash
cd ~/DAE-Second-Brain
git init
git add .
git commit -m "Initial commit"
git remote add origin <repo-url>
git push -u origin main

# Obsidian Git 플러그인이 자동으로 백업
```

### iCloud/Dropbox 백업
```
~/Library/Mobile Documents/iCloud~md~obsidian/DAE-Second-Brain
```

## 📱 모바일 접근

### Obsidian 모바일 앱
1. App Store → Obsidian 설치
2. Vault → iCloud 동기화
3. 외출 시에도 노트 확인/추가 가능!

## ❓ FAQ

**Q: 노트가 너무 많아지면 느려지나요?**
A: Obsidian은 10,000개 이상도 빠릅니다. 걱정 마세요!

**Q: Notion에서 마이그레이션 가능한가요?**
A: 네! Notion export → Markdown 변환 스크립트 사용

**Q: 팀과 공유 가능한가요?**
A: Git으로 공유 가능! Pull Request 워크플로우 사용

**Q: 검색이 느린데요?**
A: Settings → Files & Links → "Excluded files" 확인

## 🎓 추천 학습 자료

- [Obsidian 공식 문서](https://help.obsidian.md)
- [Dataview 가이드](https://blacksmithgu.github.io/obsidian-dataview/)
- [Zettelkasten 방법론](https://zettelkasten.de)
- [PARA 방법론](https://fortelabs.com/blog/para/)

---

**이제 시작할 준비가 되었습니다!** 🎉

첫 Daily Note를 만들어보세요: `Cmd + T`
