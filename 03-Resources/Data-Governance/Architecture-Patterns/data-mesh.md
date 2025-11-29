---
title: data mesh
type: resource
---

데이터 메쉬는

“데이터를 부서별로 직접 소유하고(Ownership),
제품처럼 제공(Product Thinking)하며,
셀프서브 플랫폼(Self-Serve) 위에서 운영하고,
연합형 거버넌스(Federated Governance)로 관리한다”

라는 개념입니다.

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/35cbd42f-2932-4080-8f6d-0c36c8f6649f/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46645HBO62E%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020606Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIGLImvxi5fMyCOx7iadjjPqCwBmqbM4lEq%2Bm%2FDQqgBJtAiEAqUqsBGRlqgFqcxdViIb6vbUrlpCAgdK1zElGhbPL5s0qiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDNizDPANcm4DOSW0OyrcA560equ%2FetJREZE0JjyRBkaTWJaCU%2Bg0TkzBkI9JIdGCeAZ1HUA%2FJKbpxVMGDoTUvaBGDuwU2HXrqz042sOSG%2BO7e7l%2FMu7N1zeHijAbQBlmnxBpaFl6wmsOdcgeXDj2X9MhBH0cclUKaB9XEwTlcydTKysWRS7gdhz0ye37XwNUyjD3VBG4h9aUCv9DSMofIEF3iITAjz0Pp3fbCR0krrrxjoC84quKrgsi50MVfSZy3NPxQtIQ2oamMEF07BB8qHhaMok%2FttxXHlz6xe0L51zTPmcP2CaN8K5xoc%2FXiFqskynd1gX3aMKCHFkqei3fBegFXFCkNPbMmipAdzrYdGdlF5%2FPSO%2BPGa335oUbNsIrmrKbIHi%2F6UKSotJVb2oFO21ps10AqgoUxSjDQSccDD847B4lUMPEj1%2FDEFY3FGWuzHxLkN7DKffIvEv8ADMVd%2BTG04%2Fj3Ovc%2BF7INmKPzsl9RB5eR%2BzmDBhAqVJZBXjTjj1fSVBlkuocWoJGGCE5SPMewhEpppx3KwON2yvO4lM%2FRcTVXjAnfMcEjv%2FbkImQCl8P4eG6NxdeF2OMqsX5uFnBraD9Ocm4H%2BhFwUCbcET6Aikl3zSb%2BqRhXncorsCH0TYbnGpTJp9LXA57MIKAqckGOqUBm4Aq%2FS8mWXK7Rez0AwV3OnHbe4Nqn1nR%2FyFiULK8msrXGx%2F4HFcO5Yjh10BaBLegzBT6AtHGpj4SVKGU0pQFhJ60U9Or1ZHlPVrlKUN7BRnFVIGES%2F7bNg6OrfHPuThaymWkDNAKyVCOOdGhhycq4YZObHOO57lBIauL1Fo4qndxJ0ejNUPaBNOxpLSUYT1vdcQ5alJzDbyIf7V71dXWuxcxLEZn&X-Amz-Signature=ccac535cdb6fbe494017a7cfc512b11715c55d00b95c6fa4a5f98540f9cdaa31&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 📌 데이터 메쉬(Data Mesh) 핵심 개념 요약

### 1. 도메인 중심 소유권 (Domain Ownership)

- 데이터는 IT/데이터팀이 전부 관리하는 게 아니라, 해당 데이터를 잘 아는 도메인 팀(예: 마케팅, 영업, 재무)이 직접 책임지고 관리해야 한다는 개념.
- 마치 회사가 "제품"을 각 부서에서 만드는 것처럼, 데이터도 "데이터 제품"으로 각 부서가 만든다고 보면 됨.
👉 쉽게 말해:

“내가 만든 데이터는 내가 책임진다. 대신 다른 팀도 잘 쓰게 제공한다.”

---

### 2. 데이터 = 제품 (Data as a Product)

- 데이터를 그냥 쌓아두는 게 아니라 다른 팀이 쉽게 찾고, 이해하고, 믿고 쓸 수 있는 제품(Product)처럼 제공해야 함.
- 좋은 데이터 제품의 조건: 문서화, 품질 보장, 접근 용이성, 유지보수성.
👉 쉽게 말해:

“데이터도 서비스처럼 고객(=다른 팀)을 만족시켜야 한다.”

---

### 3. 셀프서브 데이터 플랫폼 (Self-Serve Data Platform)

- 모든 도메인 팀이 데이터를 직접 제공/소비할 수 있도록, 플랫폼 팀이 공통 인프라(저장소, 카탈로그, 모니터링, 자동화 툴)를 제공해야 함.
- 덕분에 도메인 팀은 데이터 인프라를 일일이 만들 필요 없이 자기 데이터 제품에 집중할 수 있음.
👉 쉽게 말해:

“플랫폼 팀이 데이터 ‘도로’를 깔아주면, 도메인 팀은 그 위에서 자유롭게 달린다.”

---

### 4. 연합형 거버넌스 (Federated Governance)

- 중앙에서 모든 걸 통제하는 대신, 각 도메인이 자율적으로 운영하되 최소한의 공통 규칙(보안, 품질, 규제, 문서화)을 공유하는 방식.
- 즉, 표준은 중앙에서 정하고, 실행은 각 도메인이 한다는 구조.
👉 쉽게 말해:

“룰은 같이 정하고, 운영은 각자 책임진다.”

## 📌 Data Mesh 주요 구성요소 정리

### 1. Data Product (데이터 프로덕트)

- 정의: 분석·데이터 집약적 활용을 위해 도메인 팀이 책임지고 만드는 독립적인 데이터 단위.
- 구성요소: 입력 포트, 변환 코드, 저장소, 테스트, 문서화, CI/CD, 모니터링, 비용 관리 등.
- 예시:
  - BigQuery 데이터셋
  - AWS S3의 Parquet 파일
  - Azure Data Lake의 Delta 파일
  - Kafka 토픽 메시지
👉 쉽게 말해: “팀에서 관리하는 데이터 패키지(제품)”

---

### 2. Data Contract (데이터 계약)

- 정의: 데이터 제공자와 소비자 간의 데이터 교환 약속서.
- 포함 내용:
  - 제공자/소유자 정보, 접근 포트
  - 사용 조건
  - 스키마와 의미
  - 품질 속성 (freshness, row 수 등)
  - SLA (가용성, 응답 시간)
  - 비용 청구 방식
- 형식: YAML로 정의 → 스키마, SLA, 품질 검증 자동화 가능.
👉 쉽게 말해: “이 데이터는 이렇게 제공되고, 이렇게 써야 한다는 계약 문서”

---

### 3. Federated Governance (연합 거버넌스)

- 구성: 각 도메인 대표들이 모여 전사적 정책을 합의.
- 주요 정책:
  - 상호운용성 (데이터를 CSV/Parquet 등 통일된 포맷으로 제공)
  - 문서화 (소유자, 위치, 설명 필수)
  - 보안 (IAM 기반 접근제어)
  - 프라이버시, 규제 준수(Compliance)
- 특징: 중앙 통제가 아닌, 공통 규칙 + 도메인 자율 운영
👉 쉽게 말해: “룰은 같이 정하고, 실행은 각자 책임진다.”

---

### 4. Transformations (변환)

- 단계:
  - Raw 데이터 → Clean → Events → Entities → Aggregations
- Event: 변경 불가능한 사실(예: 주문 완료, 배송됨)
- Entity: 상태가 변하는 비즈니스 객체(예: 고객, 상품, 출고)
- Aggregation: 분석 목적의 요약(예: 월별 매출 합계)
- 외부 데이터: 다른 팀의 데이터 제품도 통합 가능 (anti-corruption layer 활용).
👉 쉽게 말해: “데이터를 원시 → 이벤트 → 엔티티 → 요약으로 점차 가공한다.”

---

### 5. Ingesting (인제스팅, 수집)

- 도메인 이벤트: 시스템에서 발생하는 사실들을 실시간 전송.
- 스트리밍 인제스트: Kafka, Kafka Streams, AWS Lambda 등으로 실시간 수집.
- CDC(Change Data Capture): DB 변경을 Debezium 같은 툴로 캡처.
- ELT/ETL: 배치 방식으로 파일을 가져와 적재.
👉 쉽게 말해: “데이터가 플랫폼에 들어오는 문”

---

### 6. Clean Data (데이터 정제)

- 중요성: 분석 신뢰성을 위해 데이터 정제가 필수.
- 주요 작업:
  - Structuring: 반정형 → 정형 변환 (JSON 파싱 등)
  - Mitigation: 구조 변경 시 기본값으로 보완
  - Deduplication: 중복 제거
  - Completeness: 데이터 기간 채움
  - Fix outliers: 이상치 탐지 및 보정
- 구현: SQL CTE, UDF, dbt, Apache Beam, Lambda 함수 활용.
👉 쉽게 말해: “데이터를 깔끔하게 손질하는 단계”

---

### 7. Analytics (분석)

- 방법: SQL 기반 쿼리, 조인, 윈도우 함수 → 탐색/리포트.
- 도구: Jupyter, Presto, Looker, Tableau, Metabase, Redash.
- 고급 분석: ML/AI (scikit-learn, PyTorch, TensorFlow).
👉 쉽게 말해: “데이터로 인사이트 뽑는 단계”

---

### 8. Data Platform (데이터 플랫폼)

- Self-Serve 플랫폼: 도메인 팀이 독립적으로 데이터 제품 만들고 배포할 수 있는 환경.
- 필수 기능:
  - 저장, 쿼리, 시각화, 카탈로그, 모니터링
  - Data Product 등록/발견
  - Policy Automation (PII 자동 마스킹, 표준 메타데이터 강제)
- Query Engine: BigQuery, Presto 등 → 크로스 도메인 조인 가능.
👉 쉽게 말해: “도메인 팀이 자유롭게 쓸 수 있는 데이터 놀이터”

---

### 9. Enabling Team (지원 팀)

- 역할:
  - Data Mesh 전파, 교육, 베스트 프랙티스 공유
  - 도메인 팀에 잠시 합류해 컨설턴트 역할 수행
  - 자체 데이터 제품은 만들지 않음
- 제공: 예제, 문서, 템플릿, 베스트 프랙티스.
👉 쉽게 말해: “도메인 팀이 데이터 메쉬를 잘 쓰도록 돕는 코치”