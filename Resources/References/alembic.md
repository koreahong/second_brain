---
title: alembic
created: 2025-11-28
tags: ["reference", "migrated", "resource"]
PARA: Resource
구분: []
---

# alembic

## 📝 내용

### 스키마 위치 변경시

Alembic은 기본적으로 DDL 스키마 변경 사항만 반영합니다. 즉, 테이블 추가/삭제, 컬럼 변경, 인덱스 생성 같은 것들은 --autogenerate로 잘 잡아주지만, 데이터 마이그레이션(스키마 이동 시 기존 데이터까지 자동으로 옮기는 것) 은 자동으로 생성되지 않습니다.

## 📌 왜 그런가?

- Alembic의 목적은 스키마 버전 관리에 집중되어 있습니다.

- 데이터까지 옮기려면 INSERT ... SELECT, UPDATE, COPY 같은 SQL을 직접 작성해야 합니다.

- 즉, alembic revision --autogenerate 로는 "테이블을 새 스키마에 만들라"까지만 나오고, "기존 데이터를 옮겨라"는 SQL은 직접 써줘야 해요.

## 📌 해결 방법

### 1. 수동으로 데이터 마이그레이션 SQL 추가

리비전 파일에 예를 들어 이렇게 작성할 수 있습니다:

```python
def upgrade():
    # 스키마 변경 (새 스키마에 테이블 생성)
    op.execute("CREATE SCHEMA IF NOT EXISTS mft")
    op.execute("ALTER TABLE public.users SET SCHEMA mft")

def downgrade():
    # 되돌리기 (다시 public으로)
    op.execute("ALTER TABLE mft.users SET SCHEMA public")


```

👉 ALTER TABLE ... SET SCHEMA 는 PostgreSQL에서 데이터 포함 그대로 테이블을 스키마 이동시켜줍니다. (데이터 손실 없음)

### 2. 특정 데이터만 옮기고 싶을 때

만약 테이블 구조가 바뀌고 데이터를 변환해서 옮겨야 한다면:

```python
def upgrade():
    # 새 스키마에 테이블 생성
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50)),
        schema="mft"
    )

    # 데이터 옮기기
    op.execute("""
        INSERT INTO mft.users (id, name)
        SELECT id, name FROM public.users
    """)

def downgrade():
    op.execute("""
        INSERT INTO public.users (id, name)
        SELECT id, name FROM mft.users
    """)
    op.drop_table("users", schema="mft")


```

## 📌 정리

- Alembic autogenerate → 스키마 변경만 자동

- 데이터 이동은 자동 생성 ❌, 리비전 스크립트에 직접 작성해야 함

- 단순히 스키마만 바꿀 거라면 ALTER TABLE ... SET SCHEMA가 제일 간단하고, 데이터까지 가공해서 옮길 거면 INSERT ... SELECT 문을 추가

## 🏷️ 분류

- **PARA**: Resource
- **구분**: 없음

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
