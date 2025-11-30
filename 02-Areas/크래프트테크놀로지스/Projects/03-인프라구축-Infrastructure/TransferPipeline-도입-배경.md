---
title: TransferPipeline 도입 배경
type: project-background
tags:
  - qraft
  - data-pipeline
  - refactoring
  - airflow
  - project
company: 크래프트테크놀로지스
period: 2024-12 ~ 2025-01
status: completed
created: '2025-11-30'
updated: '2025-11-30'
---
# TransferPipeline 도입 배경

## 📋 프로젝트 개요

**기간**: 2024년 12월 ~ 2025년 1월  
**담당**: Data Analytics Engineer (홍진영)  
**목적**: 데이터 적재 코드의 중복 제거 및 표준화

## 🎯 도입 배경

### 기존 문제점

크래프트테크놀로지스에서 데이터 파이프라인을 운영하면서 다음과 같은 문제가 발생했습니다:

#### 1. 코드 중복의 심각성

**상황:**
- 30개 이상의 DAG에서 동일한 SFTP → Snowflake 로직 반복
- 벤더별로 미묘하게 다른 코드 (LSEG, Bloomberg, KRX, Zeroin 등)
- 각 DAG마다 400~600줄의 boilerplate 코드

**구체적 예시:**
```python
# DAG 1: LSEG DSS Futures
@task
def load_lseg_futures():
    # SFTP 연결
    sftp_hook = SFTPHook(ssh_conn_id="sftp-lseg")
    sftp_client = sftp_hook.get_conn().open_sftp()
    
    # 파일 목록
    files = sftp_client.listdir("/tickhistory/delivered")
    csv_files = [f for f in files if f.endswith(".csv")]
    
    # 다운로드
    for file in csv_files:
        local_path = f"/tmp/{file}"
        sftp_client.get(f"/tickhistory/delivered/{file}", local_path)
        
        # Snowflake 적재
        df = pd.read_csv(local_path, sep="|")
        snowflake_hook = SnowflakeHook(snowflake_conn_id="snowflake-etl")
        snowflake_hook.insert_df(df, "FUTURES_RAW")
        
        os.remove(local_path)
    
    sftp_client.close()

# DAG 2: Bloomberg Price
@task
def load_bloomberg_price():
    # SFTP 연결 (거의 동일한 코드)
    sftp_hook = SFTPHook(ssh_conn_id="sftp-bloomberg")
    sftp_client = sftp_hook.get_conn().open_sftp()
    
    # 파일 목록 (거의 동일한 로직)
    files = sftp_client.listdir("/outbound/price")
    csv_files = [f for f in files if f.startswith("PRICE_")]
    
    # 다운로드 및 적재 (거의 동일한 로직)
    for file in csv_files:
        local_path = f"/tmp/{file}"
        sftp_client.get(f"/outbound/price/{file}", local_path)
        
        df = pd.read_csv(local_path)
        snowflake_hook = SnowflakeHook(snowflake_conn_id="snowflake-etl")
        snowflake_hook.insert_df(df, "BLOOMBERG_PRICE")
        
        os.remove(local_path)
```

**문제점:**
- 30개 DAG × 500줄 = 15,000줄의 중복 코드
- 버그 수정 시 30곳을 모두 수정해야 함
- 새로운 데이터 소스 추가 시 전체 코드 복사

#### 2. 성능 문제

**메모리 부족:**
```python
# 기존: DataFrame 전체를 메모리에 로드
df = pd.read_csv(local_path)  # 8GB CSV → 메모리 부족
snowflake_hook.insert_df(df, table_name)  # MemoryError
```

**실제 장애 사례 (2024년 11월):**
- LSEG TickHistory 데이터 (12GB CSV)
- Airflow Worker 메모리: 16GB
- 결과: `MemoryError: Unable to allocate 8.5GB`

**비효율적인 INSERT:**
```python
# Row-by-row INSERT → 45분 소요
for _, row in df.iterrows():
    conn.execute(f"INSERT INTO ... VALUES (...)")
```

#### 3. 유지보수 어려움

**변경 영향도 파악 불가:**
- 특정 벤더 API 변경 시 어떤 DAG에 영향 있는지 모름
- 전체 DAG 코드를 일일이 확인해야 함

**신규 팀원 온보딩 어려움:**
- 각 DAG마다 다른 코드 구조
- "이 DAG는 왜 이렇게 했어요?" 질문에 답변 불가

### 비즈니스 요구사항

#### 1. 데이터 소스 급증

**2024년 상반기:**
- 데이터 벤더: 5개 (LSEG, Bloomberg, KRX, Zeroin, FactSet)
- DAG 수: 12개

**2024년 하반기:**
- 데이터 벤더: 12개 (위 5개 + FRED, Invesco, SlickCharts, Kofia, 금감원, 한은, 기타)
- DAG 수: 35개

**예상 (2025년):**
- 데이터 벤더: 20개 이상
- DAG 수: 60개 이상

→ **확장성 있는 구조 필요**

#### 2. 다양한 전송 패턴

**Source 다양화:**
- SFTP (LSEG, Bloomberg)
- FTP (Zeroin)
- REST API (KRX, FRED, SlickCharts)
- Web Crawling (Invesco, 금감원)

**Target 다양화:**
- Snowflake (대부분)
- NAS (백업용)
- S3 (임시 저장)

→ **조합 가능한 구조 필요** (4 Source × 3 Target = 12가지 조합)

#### 3. 성능 요구사항

**SLA 목표:**
- 데이터 적재 시간: 2시간 이내
- 메모리 사용: Worker당 8GB 이하
- 실패율: 1% 이하

**현실:**
- 적재 시간: 평균 3.5시간 (목표 초과)
- 메모리 사용: 종종 16GB 초과 (Worker Killed)
- 실패율: 8% (메모리/타임아웃 오류)

## 💡 해결 방안: TransferPipeline

### 설계 철학

**1. Adapter 패턴 적용**
- Source와 Target을 인터페이스로 추상화
- 새로운 Source/Target 추가 시 기존 코드 변경 불필요

**2. 컨텍스트 기반 동적 처리**
- 파일명/날짜에 따라 테이블명, 컬럼 동적 결정
- 메타데이터 컬럼 자동 추가

**3. 스트리밍 방식**
- Stage-Copy 방식으로 메모리 사용 최소화
- 대용량 파일도 안정적 처리

### 구현 결정

**선택 1: Airflow Plugin으로 구현**
- 모든 DAG에서 import하여 사용
- 버전 관리 및 테스트 용이

**선택 2: Snowflake Stage-Copy 우선**
- 메모리 효율성 극대화
- Snowflake 내부 최적화 활용

**선택 3: 확장 가능한 Adapter 구조**
```
plugins/airflow_transfer/
├── interfaces.py           # 인터페이스 정의
├── transfer_pipeline.py    # 파이프라인 로직
└── adapters/
    ├── sftp_adapter.py
    ├── ftp_adapter.py
    ├── api_adapter.py
    ├── snowflake_adapter.py
    ├── nas_adapter.py
    └── s3_adapter.py
```

## 📊 도입 효과

### Before vs After

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| **코드 중복** | 15,000줄 | 2,000줄 | **-87%** |
| **평균 DAG 코드 길이** | 550줄 | 80줄 | **-85%** |
| **메모리 사용** | 평균 12GB | 평균 2GB | **-83%** |
| **적재 시간** | 평균 3.5시간 | 평균 1.2시간 | **-66%** |
| **실패율** | 8% | 0.8% | **-90%** |
| **신규 DAG 개발** | 3일 | 0.5일 | **-83%** |

### 구체적 개선 사례

#### 사례 1: LSEG DSS Futures 적재

**Before:**
```python
# 550줄 코드
# 메모리: 14GB
# 처리 시간: 45분
# 실패율: 12%
```

**After:**
```python
# 80줄 코드
source = TickHistoryAdapter(...)
target = SnowflakeAdapter(...)
pipeline = TransferPipeline(source, target)
pipeline.transfer(context_provider=get_context)

# 메모리: 1.8GB
# 처리 시간: 8분
# 실패율: 0%
```

#### 사례 2: 신규 벤더 추가 (Invesco ETF)

**Before (기존 방식):**
1. 기존 DAG 코드 복사 (550줄)
2. 벤더별 차이점 수정 (100곳 이상)
3. 테스트 (하루)
4. 리뷰 및 배포 (하루)
- **총 3일 소요**

**After (TransferPipeline):**
1. Adapter 선택 (이미 구현됨)
2. Context 함수만 작성 (20줄)
3. 테스트 및 배포 (2시간)
- **총 0.5일 소요**

```python
# 신규 DAG 전체 코드 (80줄)
@dag(
    dag_id="crawling_invesco_etf",
    schedule="@daily",
    tags=["vendor:invesco", "from:crawling", "to:snowflake", "team:Public", "datatype:fund"]
)
def crawling_invesco_etf():
    @task
    def load_etf_holdings(**kwargs):
        source = InvescoAdapter()
        target = SnowflakeAdapter(conn_id="snowflake-account-etl", database="QRAFT_ORIGIN")
        
        def get_context(filename: str) -> dict:
            return {
                "use_stage_copy": True,
                "table_name": "QRAFT_ORIGIN.INVESCO.ETF_HOLDINGS",
                "stage_name": "@FILES",
                "columns": ["ETF_TICKER", "HOLDING_TICKER", "WEIGHT", "CREATED_AT"],
                "metadata_columns": {"created_at": pendulum.now().to_datetime_string()}
            }
        
        pipeline = TransferPipeline(source, target)
        pipeline.transfer(context_provider=get_context)
```

## 🚨 도입 과정의 시행착오

### 시행착오 1: 과도한 추상화

**초기 설계 (2024년 12월):**
```python
# 너무 많은 Adapter 계층
class BaseAdapter(ABC)
    ├── RemoteAdapter(ABC)
    │   ├── SFTPAdapter
    │   └── FTPAdapter
    ├── APIAdapter(ABC)
    │   ├── RESTAdapter
    │   └── GraphQLAdapter
    └── LocalAdapter(ABC)
        ├── FileAdapter
        └── DatabaseAdapter
```

**문제:**
- 복잡도 증가
- 실제로는 2개 메서드만 필요 (list_files, read_file)

**수정 (2025년 1월):**
```python
# 단순화: 2개 인터페이스만
class SourceAdapter(ABC):
    def list_files() -> List[str]
    def read_file(remote_path, local_path)

class TargetAdapter(ABC):
    def write_data(local_path, dest_path, **kwargs)
```

### 시행착오 2: Context 설계

**초기: 클래스 기반 Context**
```python
class TransferContext:
    table_name: str
    columns: List[str]
    metadata_columns: Dict[str, str]
    # ... 20개 필드
```

**문제:**
- 모든 Adapter가 모든 필드를 이해해야 함
- 유연성 부족

**수정: Dict + kwargs 패턴**
```python
def get_context(filename: str) -> dict:
    return {"table_name": "...", "columns": [...], ...}

# TargetAdapter에서 필요한 것만 사용
def write_data(self, local_path, **kwargs):
    table_name = kwargs.get("table_name")
    columns = kwargs.get("columns", [])
```

### 시행착오 3: 팀 적용

**문제: 기존 DAG 마이그레이션 저항**
- "기존 코드도 잘 돌아가는데 왜 바꿔야 하나요?"
- "새로운 방식 학습 시간 없어요"

**해결:**
1. **Pilot 프로젝트**: 신규 DAG 3개만 먼저 적용
2. **성과 공유**: Before/After 비교 자료 Slack 공유
3. **점진적 마이그레이션**: 1주일에 5개씩 변환

**결과:**
- 1개월 후: 35개 DAG 중 25개 변환 완료
- 2개월 후: 100% 변환 완료

## 🔗 관련 문서

### 기술 문서
- [[TransferPipeline-패턴]] - 기술 구현 상세

### 프로젝트 문서
- [[qraft-data-platform-통합프로젝트]] - 전체 프로젝트 개요
- [[데이터-파이프라인-표준화]] - 파이프라인 표준화 프로젝트

### 기술 스택
- [[Airflow]] - Airflow 기술 개요
- [[Snowflake]] - Snowflake 기술 개요

---

**작성일**: 2025-11-30
**담당자**: Data Analytics Engineer
**상태**: ✅ 완료 (운영 중)
