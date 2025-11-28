---
created: 2025-11-28
type: documentation
---

# Career 폴더 구조 정리

## 📁 최종 구조

### Areas/Career/ - 실제 활동 & 경험
**용도**: 실제로 한 행동, 지원, 면접 경험

```
Areas/Career/
├── Applications/      # 지원한 회사들 (45개)
│   ├── [회사명]/
│   └── 지원 이력, 채용 공고, 커뮤니케이션 기록
│
├── Interview/         # 실제 면접 경험 (20개)
│   ├── 예상질문.md
│   ├── 그때_그때_다르게.md
│   ├── 데이터_정확도_99%.md
│   └── [면접 질문 답변, 경험 기반]
│
└── _HUB_Career.md    # Career Hub
```

**특징**:
- ✅ 실제 지원한 회사
- ✅ 실제 받았던 면접 질문
- ✅ 내가 답변한 내용
- ✅ 회사별 커뮤니케이션

---

### Knowledge/Professional-Development/ - 학습 & 준비
**용도**: 커리어 개발을 위한 지식, 학습 자료

```
Knowledge/Professional-Development/
├── Interview-Prep/    # 면접 준비 자료
│   └── 과제풀기-_하이퍼커넥트.md
│
├── Portfolio-Guide/   # 포트폴리오 작성법
│   └── 국내IT_기술블로그.md
│
├── Learning-Path/     # 커리어 패스 & 학습
│   ├── 커리어_패스_설계.md
│   ├── AI_보조_코딩_....md
│   └── Nginx_학습.md
│
└── Certifications/    # 자격증 공부
    ├── 1과목.md
    ├── 2과목.md
    └── 3과목.md
```

**특징**:
- ✅ 일반적인 면접 준비 방법
- ✅ 포트폴리오 작성 가이드
- ✅ 커리어 개발 전략
- ✅ 자격증 학습 자료

---

## 🔄 차이점 요약

| | Areas/Career | Knowledge/Professional-Development |
|---|---|---|
| **성격** | 실제 활동 | 지식/학습 |
| **내용** | 지원한 회사, 면접 경험 | 준비 방법, 가이드 |
| **예시** | "토스 면접 질문" | "면접 준비하는 방법" |
| | "네이버 지원 이력" | "이력서 작성법" |
| **타입** | Experience | Concept/Pattern |

---

## 💡 사용 예시

### 새 회사 지원할 때

1. **먼저**: `Knowledge/Professional-Development/Interview-Prep/` 에서 준비 방법 확인
2. **그 다음**: `Areas/Career/Applications/[회사명]/` 폴더 생성
3. **면접 후**: `Areas/Career/Interview/` 에 경험 기록

### 면접 준비할 때

1. **일반적인 준비**: `Knowledge/Professional-Development/Interview-Prep/`
2. **내 경험 복습**: `Areas/Career/Interview/` (과거 면접 질문들)
3. **회사 정보**: `Areas/Career/Applications/[회사명]/`

---

## 🔗 연결 구조

```
Knowledge/Professional-Development/Interview-Prep/
   ↓ (학습 후 실제 적용)
Areas/Career/Applications/[회사명]/
   ↓ (면접 경험)
Areas/Career/Interview/[면접질문].md
   ↓ (패턴 추출)
Knowledge/Professional-Development/Interview-Prep/[새로운 패턴].md
```

---

## 📝 템플릿

### 회사 지원 노트
```markdown
---
type: application
company: [회사명]
position: Data Engineer
status: [지원중|면접|합격|불합격]
date: 2025-11-28
---

# [회사명] 지원

## 회사 정보
- 규모:
- 업종:
- 기술 스택:

## 포지션
- 직무:
- 요구 사항:

## 지원 과정
- 지원일:
- 서류 결과:
- 면접 일정:

## 준비 사항
- [ ] 이력서 커스터마이징
- [ ] 포트폴리오 준비
- [ ] 기술 질문 준비

## 면접 기록
[[면접-YYYY-MM-DD]]

## 결과
-
```

### 면접 경험 노트
```markdown
---
type: interview-experience
company: [회사명]
date: 2025-11-28
result: [합격|불합격|대기]
---

# [회사명] 면접 - YYYY-MM-DD

## 면접 정보
- 단계: 1차/2차/최종
- 면접관: n명
- 시간: n분

## 질문 & 답변

### 기술 질문
**Q**:
**A**:

### 경험 질문
**Q**:
**A**:

## 잘한 점
-

## 아쉬운 점
-

## 배운 점
-

## 관련 노트
- [[기술 개념]]
- [[프로젝트]]
```

---

*Last Updated: 2025-11-28*
*Purpose: Career vs Professional-Development 구분*
