---
title: Snowflake Storage Integration
type: resource
tags:
  - snowflake
  - storage-integration
  - s3
  - external-stage
  - file-format
  - iam
  - aws
created: '2025-11-30'
updated: '2025-11-30'
aliases:
  - Snowflake S3 Integration
status: evergreen
maturity: 3
---
# Snowflake Storage Integration

## 📌 개요

Snowflake와 외부 스토리지(S3)를 연결하여 데이터를 자동으로 적재하는 방법을 설명합니다.

## 🎓 핵심 개념

### Storage Integration이란?

Snowflake와 외부 클라우드 스토리지(S3, Azure Blob, GCS)를 안전하게 연결하는 Snowflake 객체

**주요 목적:**
- AWS IAM Role 기반 인증 (Access Key 불필요)
- 중앙화된 권한 관리
- 여러 Stage에서 재사용 가능

### External Stage란?

외부 스토리지의 파일을 Snowflake 테이블로 로드하기 위한 경로

**특징:**
- Storage Integration 사용
- File Format 지정
- COPY INTO 명령으로 데이터 적재
- Directory 메타데이터 활성화 가능

### File Format이란?

파일의 구조를 정의하는 Snowflake 객체

**지원 형식:**
- CSV, JSON, AVRO, ORC, PARQUET, XML

---

## 🏗️ 전체 아키텍처

```
┌─────────────────┐
│   AWS S3        │
│  Bucket         │
└────────┬────────┘
         │
         │ IAM Role (sts:AssumeRole)
         │ ExternalId 검증
         ▼
┌─────────────────┐
│  Storage        │
│  Integration    │  ← Snowflake 객체
└────────┬────────┘
         │
         │ 1개 Integration → N개 Stages
         ▼
┌─────────────────┐
│  External       │
│  Stage          │  ← File Format 사용
└────────┬────────┘
         │
         │ COPY INTO
         ▼
┌─────────────────┐
│  Snowflake      │
│  Table          │
└─────────────────┘
```

---

## 🔧 구현 단계

### Step 1: File Format 생성

```sql
CREATE FILE FORMAT qraft_origin.staging.portpolio_rebalancing_csv_format
  TYPE = CSV
  RECORD_DELIMITER = '\n'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  PARSE_HEADER = FALSE
  DATE_FORMAT = 'AUTO'
  TIME_FORMAT = 'AUTO'
  TIMESTAMP_FORMAT = 'AUTO'
  BINARY_FORMAT = 'HEX'
  ESCAPE = 'NONE'
  ESCAPE_UNENCLOSED_FIELD = '\\'
  TRIM_SPACE = FALSE
  FIELD_OPTIONALLY_ENCLOSED_BY = 'NONE'
  NULL_IF = ('\\N')
  COMPRESSION = 'AUTO'
  ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
  VALIDATE_UTF8 = TRUE
  SKIP_BLANK_LINES = TRUE
  REPLACE_INVALID_CHARACTERS = FALSE
  EMPTY_FIELD_AS_NULL = TRUE
  SKIP_BYTE_ORDER_MARK = TRUE
  ENCODING = 'UTF8';
```

**주요 옵션:**
- `SKIP_HEADER = 1`: 첫 번째 행(헤더) 건너뛰기
- `ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE`: 컬럼 수 불일치 허용
- `EMPTY_FIELD_AS_NULL = TRUE`: 빈 필드를 NULL로 처리

### Step 2: Storage Integration 생성

```sql
CREATE STORAGE INTEGRATION portpolio_rebalancing
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::717473574740:role/snowflake-integration-portpolio-rebalancing'
  STORAGE_ALLOWED_LOCATIONS = ('s3://portpolio-rebalancing/')
  COMMENT = 'Snowflake <-> Qraft S3 connection for rebalancing data';
```

**주요 속성:**
- `STORAGE_AWS_ROLE_ARN`: Snowflake가 Assume할 IAM Role
- `STORAGE_ALLOWED_LOCATIONS`: 접근 가능한 S3 경로 (화이트리스트)

### Step 3: ExternalId 확인

```sql
DESC STORAGE INTEGRATION portpolio_rebalancing;
```

**출력에서 확인할 항목:**
- `STORAGE_AWS_IAM_USER_ARN`: Snowflake의 IAM User ARN
- `STORAGE_AWS_EXTERNAL_ID`: AWS Trust Policy에 사용할 ExternalId

### Step 4: AWS IAM Role Trust Policy 설정

**AWS Console → IAM → Roles → snowflake-integration-portpolio-rebalancing → Trust relationships**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::530467106055:user/s1q00000-s"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "DOB17693_SFCRole=3_K1F0kYECV5J9cdIi6aO4462BUkk="
                }
            }
        }
    ]
}
```

**중요:**
- `AWS`: Snowflake IAM User ARN (Step 3에서 확인)
- `sts:ExternalId`: Snowflake External ID (Step 3에서 확인)

### Step 5: External Stage 생성

```sql
CREATE STAGE qraft_origin.staging.portpolio_rebalancing
  URL = 's3://portpolio-rebalancing/'
  STORAGE_INTEGRATION = portpolio_rebalancing
  FILE_FORMAT = (FORMAT_NAME = qraft_origin.staging.portpolio_rebalancing_csv_format)
  COMMENT = 'Stage for portfolio rebalancing CSV files';
```

### Step 6: Directory 메타데이터 활성화

```sql
ALTER STAGE qraft_origin.staging.portpolio_rebalancing 
SET DIRECTORY = (ENABLE = TRUE);
```

**Directory 기능:**
- 파일 메타데이터를 Snowflake 테이블처럼 쿼리 가능
- `RELATIVE_PATH`, `SIZE`, `LAST_MODIFIED` 등 정보 제공
- JOIN 연산 가능

---

## 🔍 Stage 파일 조회 방법

### 방법 1: LIST (실시간 조회)

```sql
LIST @qraft_origin.staging.portpolio_rebalancing;
```

**특징:**
- ✅ 실시간으로 S3 스캔
- ✅ REFRESH 불필요
- ❌ 쿼리 결과를 JOIN할 수 없음
- ❌ 파일 수가 많으면 느림

**사용 시점:**
- 빠르게 파일 목록 확인
- 파일 존재 여부 체크

### 방법 2: DIRECTORY (메타데이터 테이블)

```sql
-- 1. 먼저 메타데이터 갱신 필요
ALTER STAGE qraft_origin.staging.portpolio_rebalancing REFRESH;

-- 2. 쿼리 (테이블처럼 사용 가능)
SELECT 
    RELATIVE_PATH,
    SIZE,
    LAST_MODIFIED
FROM DIRECTORY(@qraft_origin.staging.portpolio_rebalancing)
WHERE RELATIVE_PATH LIKE '%2025-09-30.csv%'
LIMIT 10;
```

**특징:**
- ✅ 빠른 쿼리 (메타데이터 테이블)
- ✅ JOIN 가능
- ✅ WHERE, ORDER BY 등 SQL 연산 가능
- ❌ `REFRESH` 필요 (실시간 아님)

**사용 시점:**
- 복잡한 쿼리 (JOIN, 집계)
- 파일 수가 많을 때
- 정기적으로 갱신되는 경우

### LIST vs DIRECTORY 비교

| 기능 | LIST | DIRECTORY |
|------|------|-----------|
| 실시간 | ✅ Yes | ❌ No (REFRESH 필요) |
| JOIN | ❌ No | ✅ Yes |
| 속도 | 느림 (S3 스캔) | 빠름 (메타데이터) |
| SQL 연산 | ❌ 제한적 | ✅ 전체 지원 |
| 사용 예 | 파일 존재 확인 | 복잡한 필터링 |

---

## 💻 실전 사용 예시

### 예시 1: 특정 포트폴리오의 최신 파일 찾기

```sql
-- 1. 메타데이터 갱신
ALTER STAGE qraft_origin.staging.portpolio_rebalancing REFRESH;

-- 2. 파일 조회 (포트폴리오별 JOIN)
SELECT 
    p.portid,
    d.RELATIVE_PATH AS file_path,
    d.SIZE,
    d.LAST_MODIFIED
FROM (
    SELECT DISTINCT SUBSTRING(PORTID, 1, LENGTH(PORTID) - 1) AS portid
    FROM qraft_origin.mart.port_meta
    WHERE teams = 'strategy' 
        AND use_yn = 'Y'
) p
LEFT JOIN DIRECTORY(@qraft_origin.staging.portpolio_rebalancing) d
    ON d.RELATIVE_PATH LIKE '%' || p.portid || '/%' || p.portid || '_%'
    AND d.RELATIVE_PATH LIKE '%2025-09-30.csv'
ORDER BY p.portid;
```

**설명:**
- `port_meta` 테이블의 포트폴리오 목록과 JOIN
- S3 파일 경로 패턴 매칭
- 특정 날짜 파일만 필터링

### 예시 2: LIST 결과를 RESULT_SCAN으로 재활용

```sql
-- 1. LIST 실행
LIST @zeroin.public.zeroin_fund_fdtcd001_migration;

-- 2. 바로 이전 쿼리 결과 재사용
SELECT *
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
WHERE "name" LIKE '%FDTCD001.20251015%';
```

**주의:**
- `RESULT_SCAN`은 바로 이전 쿼리 결과만 참조
- 컬럼명이 대소문자 구분 (따옴표 필요)

---

## 🛠️ 유지보수

### Storage Integration 수정

```sql
-- 허용 경로 변경
ALTER STORAGE INTEGRATION portpolio_rebalancing
SET STORAGE_ALLOWED_LOCATIONS = ('s3://portpolio-rebalancing/', 's3://new-bucket/');

-- Integration 비활성화
ALTER STORAGE INTEGRATION portpolio_rebalancing SET ENABLED = FALSE;
```

### Stage 삭제 및 재생성

```sql
-- Stage 삭제
DROP STAGE qraft_origin.staging.portpolio_rebalancing;

-- Storage Integration 삭제
DROP STORAGE INTEGRATION portpolio_rebalancing;
```

---

## 🔐 보안 모범 사례

1. **최소 권한 원칙**
   - `STORAGE_ALLOWED_LOCATIONS`를 특정 경로로 제한
   - IAM Role에 필요한 S3 버킷만 허용

2. **ExternalId 사용**
   - AWS Trust Policy에 ExternalId 조건 필수
   - Confused Deputy 공격 방지

3. **Storage Integration 재사용**
   - 여러 Stage에서 동일한 Integration 사용
   - 중앙화된 권한 관리

---

## 📎 Related

### Technology (Core Concepts)
- [[Snowflake]] - Snowflake 기본 개념 및 Qraft 적용 사례

### Technology (Related Implementation)
- [[Snowflake-RBAC-가이드]] - Snowflake 권한 관리 개념
- [[DBT-구현]] - DBT에서 External Stage 사용
- [[TransferPipeline-패턴]] - S3 → Snowflake 데이터 전송

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/Active/qraft-data-platform-통합프로젝트|qraft-data-platform-통합프로젝트]] - Data Platform에서 S3 연동

---

**Metadata:**
