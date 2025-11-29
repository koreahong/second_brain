---
title: "Jira 개념"
source: notion
notion_id: 25cc6d43-3b4d-8006-8fc5-fa6bf0a1f773
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["JIRA"]
링크: []
최종편집시각: "2025-08-27T08:33:00.000Z"
제목: ""
상위 항목: []
PARA: "Resource"
tags: ["JIRA", "레퍼런스", "notion-import"]
---

## 🧱 Jira 이슈 타입 구조 정리 (기본적인 계층 포함)

### 🔵 1. Epic

- 의미: 큰 기능 또는 목표. 여러 Story나 Task를 포함하는 상위 작업.
- 용도: 제품의 큰 기능, 스프린트의 핵심 목표 등
- 예시: "모바일 앱 로그인 기능 개발"
---

### 🟢 2. Story

- 의미: 사용자의 관점에서 작성된 기능 요구사항 (User Story)
- Epic의 하위 항목
- 용도: 개발자가 작업할 수 있는 기능 단위
- 예시: "사용자는 이메일과 비밀번호로 로그인할 수 있어야 한다"
---

### 🟡 3. Task

- 의미: 일반적인 작업 단위 (기능, 비기능, 분석 등)
- Epic에 귀속되기도 하고 독립되기도 함
- 용도: Story와 비슷하지만 사용자 관점이 아닐 수도 있음
- 예시: "데이터베이스 스키마 설계"
---

### 🔻 4. Sub-task

- 의미: Story나 Task를 더 세분화한 작업
- 상위 이슈에 종속됨
- 용도: 세부 작업 관리
- 예시: "로그인 화면 UI 구현", "API 연결"
---

### 🔴 5. Bug

- 의미: 기능 결함, 문제점
- Story나 Task의 하위에 두기도 함
- 용도: QA 중 발견된 문제 추적
- 예시: "비밀번호 오류 시 잘못된 메시지가 출력됨"
---

## 🧩 계층 구조 (Hierarchy 예시)

```plain text
Epic
 ├── Story 1
 │    ├── Sub-task A
 │    ├── Sub-task B
 ├── Story 2
 │    ├── Sub-task C
 ├── Task 1
 │    ├── Sub-task D


```

# Jira connections

