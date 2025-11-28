---
title: sqs redrive & dlq
created: 2025-11-28
tags: ["reference", "migrated", "aws", "sqs", "lambda"]
PARA: 
구분: ["AWS", "SQS", "Lambda"]
---

# sqs redrive & dlq

## 📝 내용

## 개념

- sqs + lambda 진행시 소화하지 못한 메세지는 dead lock queue로 빠지게 하거나 redrive를 해야함.

## 목적

- 람다로 요청한 메세지들에 대한 관리

## 서칭내용

### 일반 큐와 dlq 연결

- 일반 메세지 큐 세팅

- 배달 못한 편지 대기열 세팅

docker build -t lambda_container -f dockerfile_lambda .

## 🏷️ 분류

- **PARA**: 
- **구분**: AWS, SQS, Lambda

## 🔗 연결

**Hub**: [[_HUB_Infrastructure]], [[_HUB_Python]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
