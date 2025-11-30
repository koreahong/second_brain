---
title: TransferPipeline 패턴
type: technical-pattern
tags:
  - airflow
  - adapter-pattern
  - data-pipeline
  - etl
  - python
created: '2025-11-30'
updated: '2025-11-30'
status: evergreen
---
# TransferPipeline 패턴

## 📋 개요

TransferPipeline은 **Adapter 패턴**을 활용한 데이터 전송 추상화 레이어입니다. Source(출처) → Target(목적지) 간 데이터 이동을 표준화하여, 다양한 데이터 소스와 타겟을 조합할 수 있는 유연한 구조를 제공합니다.

**핵심 개념:**
- **SourceAdapter**: 데이터를 읽는 역할 (SFTP, FTP, API 등)
- **TargetAdapter**: 데이터를 쓰는 역할 (Snowflake, NAS, S3 등)
- **TransferPipeline**: Source와 Target을 연결하는 파이프라인

## 🎯 Adapter 패턴 적용

### 인터페이스 정의

```python
# plugins/airflow_transfer/interfaces.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any

class SourceAdapter(ABC):
    """데이터 읽기 인터페이스"""
    
    @abstractmethod
    def list_files(self) -> List[str]:
        """파일 목록 조회"""
        pass
    
    @abstractmethod
    def read_file(self, remote_path: str, local_path: Path):
        """파일 다운로드"""
        pass
    
    def open(self):
        """연결 열기 (선택)"""
        pass
    
    def close(self):
        """연결 닫기 (선택)"""
        pass


class TargetAdapter(ABC):
    """데이터 쓰기 인터페이스"""
    
    @abstractmethod
    def write_data(self, local_path: Path, dest_path: str, **kwargs):
        """데이터 적재"""
        pass
    
    def open(self):
        """연결 열기 (선택)"""
        pass
    
    def close(self):
        """연결 닫기 (선택)"""
        pass
```

### Pipeline 구현

```python
# plugins/airflow_transfer/transfer_pipeline.py

class TransferPipeline:
    def __init__(self, source: SourceAdapter, target: TargetAdapter):
        self.source = source
        self.target = target
    
    def transfer(
        self,
        dest_base: str = "",
        context_provider: Optional[Callable[[str], Dict[str, Any]]] = None,
        transformer: Optional[Callable[[Path], Path]] = None,
    ):
        """
        Source → Target 데이터 전송
        
        Args:
            dest_base: 대상 경로
            context_provider: 파일별 추가 컨텍스트 (테이블명, 컬럼 등)
            transformer: 파일 변환 함수 (JSON→Parquet 등)
        """
        # 1. 연결 열기
        if hasattr(self.source, "open"):
            self.source.open()
        if hasattr(self.target, "open"):
            self.target.open()
        
        # 2. 파일 목록 조회
        files = self.source.list_files()
        
        try:
            for remote_path in files:
                filename = os.path.basename(remote_path)
                
                # 3. 컨텍스트 가져오기
                context = context_provider(filename) if context_provider else {}
                
                # 4. 임시 파일로 다운로드
                tmp_path = Path(tempfile.gettempdir()) / filename
                self.source.read_file(remote_path, tmp_path)
                
                # 5. 변환 (옵션)
                upload_path = transformer(tmp_path) if transformer else tmp_path
                
                # 6. 타겟에 업로드
                dest_path = context.get("dest_path", os.path.join(dest_base, filename))
                self.target.write_data(upload_path, dest_path, **context)
                
                # 7. 임시 파일 삭제
                if tmp_path.exists():
                    tmp_path.unlink()
        
        finally:
            # 8. 연결 닫기
            if hasattr(self.source, "close"):
                self.source.close()
            if hasattr(self.target, "close"):
                self.target.close()
```

## 🔌 구현된 Adapter들

### SourceAdapter 구현체

#### 1. SFTPAdapter
```python
from plugins.airflow_transfer.adapters import SFTPAdapter

source = SFTPAdapter(
    conn_id="sftp-vendor",
    base_path="/data/files",
    filter_fn=lambda f: f.endswith(".csv")
)
```

#### 2. TickHistoryAdapter (LSEG DSS API)
```python
from plugins.airflow_transfer.adapters import TickHistoryAdapter

source = TickHistoryAdapter(
    schedule_name="daily_qraft_data_futures",
    extracted_file_name="daily_qraft_data_futures_20250129.csv"
)
```

#### 3. KRXApiAdapter
```python
from plugins.airflow_transfer.adapters import KRXApiAdapter

source = KRXApiAdapter(
    api_key=Variable.get("krx_api_key"),
    endpoint="/equities/ohlcv"
)
```

### TargetAdapter 구현체

#### 1. SnowflakeAdapter

**3가지 적재 방식 지원:**

##### 방식 1: Direct Insert (기본)
```python
target = SnowflakeAdapter(
    conn_id="snowflake-account-etl",
    database="QRAFT_ORIGIN",
    table_name="raw_data"
)

# DataFrame을 바로 INSERT
pipeline.transfer()
```

##### 방식 2: Stage-Copy (대용량 일괄 적재)
```python
def get_context(filename):
    return {
        "use_stage_copy": True,
        "table_name": "QRAFT_ORIGIN.LSEG_DSS.FUTURES_1D_TEMP",
        "stage_name": "@QRAFT_ORIGIN.LSEG_DSS.TICKHISTORY",
        "columns": ["TRADE_DATE", "RIC", "OPEN", "HIGH", "LOW", "CLOSE"],
        "metadata_columns": {
            "created_at": "2025-01-29 10:00:00"
        },
        "truncate_before_copy": True
    }

pipeline.transfer(context_provider=get_context)
```

**처리 흐름:**
```
1. 파일 → Stage 업로드 (PUT)
2. 메타데이터 컬럼 추가 (created_at 등)
3. TRUNCATE TABLE (옵션)
4. COPY INTO로 적재
```

##### 방식 3: Stage-Merge (Upsert)
```python
def get_context(filename):
    return {
        "use_stage_merge": True,
        "table_name": "QRAFT_ORIGIN.CORE.DIM_TICKER",
        "stage_name": "@FILES",
        "columns": ["TICKER", "NAME", "SECTOR"],
        "comp_cols": ["TICKER"],  # MERGE 비교 컬럼
        "transform_fn": lambda df: preprocess_ticker(df)
    }

pipeline.transfer(context_provider=get_context)
```

**처리 흐름:**
```
1. 파일 → Stage 업로드
2. 변환 함수 적용 (옵션)
3. COPY INTO temp 테이블
4. MERGE (comp_cols 기준)
   - 존재하면 UPDATE
   - 없으면 INSERT
```

#### 2. NASAdapter
```python
target = NASAdapter(
    base_path="/mnt/nas-quant/short-term/krx/equities/ohlcv/daily/raw"
)
```

## 📝 사용 예시

### 예시 1: SFTP → Snowflake (일괄 적재)

```python
from plugins.airflow_transfer.adapters import SFTPAdapter, SnowflakeAdapter
from plugins.airflow_transfer.transfer_pipeline import TransferPipeline

@task
def load_vendor_data(**kwargs):
    # Source: SFTP
    source = SFTPAdapter(
        conn_id="sftp-vendor",
        base_path="/outbound",
        filter_fn=lambda f: f.startswith("daily_") and f.endswith(".csv")
    )
    
    # Target: Snowflake
    target = SnowflakeAdapter(
        conn_id="snowflake-account-etl",
        database="QRAFT_ORIGIN"
    )
    
    # Context: 파일명에서 날짜 추출
    def get_context(filename: str) -> dict:
        # daily_20250129.csv → 20250129
        date_str = filename.split("_")[1].split(".")[0]
        
        return {
            "use_stage_copy": True,
            "table_name": "QRAFT_ORIGIN.VENDOR.RAW_DATA",
            "stage_name": "@FILES",
            "columns": ["DATE", "SYMBOL", "PRICE", "VOLUME", "CREATED_AT"],
            "metadata_columns": {
                "date": date_str,
                "created_at": pendulum.now().to_datetime_string()
            },
            "truncate_before_copy": False  # Append
        }
    
    # Pipeline 실행
    pipeline = TransferPipeline(source, target)
    copied = pipeline.transfer(context_provider=get_context)
    
    logger.info(f"✅ {copied} files transferred")
```

### 예시 2: API → Snowflake (변환 포함)

```python
import pandas as pd
from pathlib import Path

@task
def fetch_krx_ohlcv(**kwargs):
    source = KRXApiAdapter(
        api_key=Variable.get("krx_api_key"),
        endpoint="/equities/ohlcv"
    )
    
    target = SnowflakeAdapter(
        conn_id="snowflake-account-etl",
        database="QRAFT_ORIGIN"
    )
    
    # Transformer: JSON → Parquet 변환
    def json_to_parquet(json_path: Path) -> Path:
        df = pd.read_json(json_path)
        
        # 데이터 변환
        df['TRADE_DATE'] = pd.to_datetime(df['date'])
        df['TICKER'] = df['symbol']
        
        # Parquet 저장
        parquet_path = json_path.with_suffix('.parquet')
        df.to_parquet(parquet_path, index=False)
        
        return parquet_path
    
    def get_context(filename: str) -> dict:
        return {
            "use_stage_copy": True,
            "table_name": "QRAFT_ORIGIN.KRX.EQUITIES_OHLCV_DAILY",
            "stage_name": "@FILES",
            "columns": ["TRADE_DATE", "TICKER", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"],
            "file_format": "TYPE = 'PARQUET'"
        }
    
    pipeline = TransferPipeline(source, target)
    pipeline.transfer(context_provider=get_context, transformer=json_to_parquet)
```

### 예시 3: SFTP → NAS (파일 백업)

```python
@task
def backup_to_nas(**kwargs):
    source = SFTPAdapter(
        conn_id="sftp-lseg",
        base_path="/tickhistory/delivered",
        filter_fn=lambda f: f.endswith(".csv.gz")
    )
    
    target = NASAdapter(
        base_path="/mnt/nas-quant/backup/lseg/tickhistory"
    )
    
    pipeline = TransferPipeline(source, target)
    pipeline.transfer()
```

## ⚠️ 트라이 에러

### 문제 1: 대용량 파일 메모리 부족

**증상:**
```
MemoryError: Unable to allocate array with shape (10000000, 50)
```

**원인:** DataFrame 전체를 메모리에 로드 후 Snowflake INSERT

**해결:**
```python
# ❌ Before: Direct Insert (메모리 사용)
df = pd.read_csv(local_path)
target.write_data_direct(df, table_name)

# ✅ After: Stage-Copy (스트리밍)
context = {
    "use_stage_copy": True,
    "table_name": "...",
    "stage_name": "@FILES"
}
target.write_data(local_path, **context)
```

**효과:**
- 메모리 사용량: 8GB → 500MB
- 처리 시간: 45분 → 8분

### 문제 2: COPY INTO 중복 실행

**증상:**
```
Duplicate row detected: TICKER='AAPL', DATE='2025-01-29'
```

**원인:** 
- `truncate_before_copy=False`로 Append 모드
- 재실행 시 동일 데이터 중복 적재

**해결:**
```python
# 방법 1: Truncate 사용 (전체 삭제 후 적재)
context = {
    "truncate_before_copy": True  # 기존 데이터 삭제
}

# 방법 2: Stage-Merge 사용 (Upsert)
context = {
    "use_stage_merge": True,
    "comp_cols": ["TICKER", "TRADE_DATE"]  # 중복 체크 컬럼
}
```

### 문제 3: Metadata 컬럼 순서 불일치

**증상:**
```
SQL compilation error: Column 'CREATED_AT' does not exist in table
```

**원인:** `columns` 리스트와 실제 CSV 컬럼 순서 불일치

**해결:**
```python
# ✅ 정확한 컬럼 순서 지정
context = {
    "columns": [
        "TRADE_DATE",   # 원본 CSV: 1번째 컬럼
        "TICKER",       # 원본 CSV: 2번째 컬럼
        "PRICE",        # 원본 CSV: 3번째 컬럼
        "CREATED_AT"    # metadata_columns로 추가
    ],
    "metadata_columns": {
        "created_at": "2025-01-29"
    }
}
```

**SnowflakeAdapter 내부 처리:**
```python
# 1. 원본 CSV 읽기 (헤더 없음)
df_original = pd.read_csv(local_path, sep="|", header=None)
# → [0, 1, 2] 컬럼 (TRADE_DATE, TICKER, PRICE)

# 2. columns 순서대로 재구성
result_data = {}
original_col_idx = 0

for col_name in columns:  # ["TRADE_DATE", "TICKER", "PRICE", "CREATED_AT"]
    if col_name.lower() in metadata_columns:
        # 메타데이터 컬럼
        result_data[col_name] = [metadata_columns[col_name.lower()]] * len(df)
    else:
        # 원본 데이터 컬럼
        result_data[col_name] = df_original[original_col_idx].tolist()
        original_col_idx += 1

# 3. 새 DataFrame 생성 및 저장
df_new = pd.DataFrame(result_data)
df_new.to_csv(local_path, header=False, sep="|")
```

### 문제 4: SFTP 연결 타임아웃

**증상:**
```
paramiko.ssh_exception.SSHException: Timeout opening channel
```

**원인:** 
- 대량 파일 전송 중 연결 유지 시간 초과
- `list_files()` 후 오래 걸려서 연결 끊김

**해결:**
```python
class SFTPAdapter(SourceAdapter):
    def __init__(self, conn_id, base_path, filter_fn=None, keepalive_interval=60):
        self.keepalive_interval = keepalive_interval
    
    def open(self):
        self.conn = self.hook.get_conn()
        self.sftp = self.conn.open_sftp()
        
        # Keep-alive 설정
        transport = self.conn.get_transport()
        transport.set_keepalive(self.keepalive_interval)
    
    def list_files(self):
        # 타임아웃 방지: 연결 상태 확인
        if not self.sftp or not self.conn.get_transport().is_active():
            self.open()
        
        return super().list_files()
```

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/TransferPipeline-도입-배경|TransferPipeline-도입-배경]] - 왜 이 패턴이 필요했는가

### Technology (Core Concepts)
- [[Airflow]] - Airflow 기본 개념 및 Qraft 적용 사례
- [[Snowflake]] - Snowflake Data Warehouse

### Technology (Related Implementation)
- [[Airflow-3.0-구현]] - Airflow 3.0 플랫폼 구현
- [[DBT-구현]] - DBT 데이터 변환

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/Active/qraft-data-platform-통합프로젝트|qraft-data-platform-통합프로젝트]] - Data Platform에서 실제 사용

---

**작성일**: 2025-11-30
**카테고리**: Data Engineering Pattern
**태그**: #airflow #adapter-pattern #data-pipeline #etl
