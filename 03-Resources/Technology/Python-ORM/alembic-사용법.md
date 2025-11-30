---
title: alembic 사용법
type: resource
tags:
  - alembic
  - db
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 개념

- alembic은 스키마 동기화하는 도구임
## 목적

- 쇼핑몰간의 스키마 동기화를 하기 위함
- 컬럼 한 개를 수정하려면 모든몰에 영향을 끼치는 환경에서 효율적인 관리방법을 찾기 위함임
## 서칭내용

### 구조

- alembic의 구조는 간단하다.

alembic을 실행하면 테이블은 models에 정의한대로 업데이트된다.

업데이트 과정에서 진행된 변경사항이 파일로 생성이 된다.
- alembic은 테이블/컬럼의 삭제 및 추가한 내역만 자동으로 변환관리를 한다,

따라서, 이름 변경, 제약조건 등등의 변경 사항은 사용자가 집적 버전관리 파일에 변경해야하는 내용에 맞게 작성해야 한다.
### 사용법

- alembic은 버전관리를 하기 위해서 각 버전관리 파일마다 이전버전의 코드를 기록한다
- upgrade에는 변경사항에 대한 코드를 작성하고 downgrade에는 변경사항을 원복하는 코드를 작성한다
```javascript
pip install alembic

alembic init migrations -- 초기 alembic 시작

-- 변경기록 시작
** 스키마를 수정하기 전에 반드시 해당 코드를 실행하고 진행해야 함
alembic revision -m "{commit 메세지}"

-- 변경사항 작성, upgrade, downgrade

1. 테이블 생성 및 삭제
	def upgrade():
	    # 테이블 생성
	    op.create_table(
	        'users',
	        sa.Column('id', sa.Integer, primary_key=True),
	        sa.Column('name', sa.String(50), nullable=False),
	        sa.Column('email', sa.String(100), unique=True),
	        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
	    )
	
	def downgrade():
	    # 테이블 삭제
	    op.drop_table('users')

2. 컬럼 추가 및 삭제
	def upgrade():
	    # 컬럼 추가
	    op.add_column('users', sa.Column('age', sa.Integer))
	
	def downgrade():
	    # 컬럼 삭제
	    op.drop_column('users', 'age')

3. 컬럼 이름 변경
	def upgrade():
	    # 컬럼 이름 변경
	    op.alter_column('users', 'old_column_name', new_column_name='new_column_name')
	
	def downgrade():
	    # 원래 이름으로 복원
	    op.alter_column('users', 'new_column_name', new_column_name='old_column_name')
   
4. 컬럼 데이터 타입 변경   
	def upgrade():
    # 데이터 타입 변경 (예: Integer → String)
    op.alter_column('users', 'age', type_=sa.String(50))

	def downgrade():
	    # 원래 데이터 타입으로 복원
	    op.alter_column('users', 'age', type_=sa.Integer)
	    
5. 기본값 설정 및 제거
def upgrade():
    # 기본값 추가
    op.alter_column('users', 'age', server_default='18')

def downgrade():
    # 기본값 제거
    op.alter_column('users', 'age', server_default=None)

6. 프라이머리 키 변경
def upgrade():
    # 기존 프라이머리 키 삭제
    op.drop_constraint('pk_users', 'users', type_='primary')
    
    # 새로운 프라이머리 키 추가
    op.create_primary_key('pk_users_new', 'users', ['new_id_column'])

def downgrade():
    # 원래 프라이머리 키로 복원
    op.drop_constraint('pk_users_new', 'users', type_='primary')
    op.create_primary_key('pk_users', 'users', ['id'])

7. 외래 키 추가 및 제거
def upgrade():
    # 외래 키 추가
    op.create_foreign_key('fk_user_role', 'users', 'roles', ['role_id'], ['id'])

def downgrade():
    # 외래 키 제거
    op.drop_constraint('fk_user_role', 'users', type_='foreignkey')

8. 고유 제약조건 추가 및 제거
def upgrade():
    # 고유 제약조건 추가
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

def downgrade():
    # 고유 제약조건 제거
    op.drop_constraint('uq_users_email', 'users', type_='unique')

9. 체크 제약조건 추가 및 제거
def upgrade():
    # 체크 제약조건 추가
    op.create_check_constraint('ck_user_age_positive', 'users', sa.text('age > 0'))

def downgrade():
    # 체크 제약조건 제거
    op.drop_constraint('ck_user_age_positive', 'users', type_='check')

10. 인덱스 추가 및 제거
def upgrade():
    # 인덱스 추가
    op.create_index('ix_users_name', 'users', ['name'])

def downgrade():
    # 인덱스 제거
    op.drop_index('ix_users_name', 'users')

11. 테이블 이름 변경
def upgrade():
    # 테이블 이름 변경
    op.rename_table('old_table_name', 'new_table_name')

def downgrade():
    # 원래 이름으로 복원
    op.rename_table('new_table_name', 'old_table_name')

12. 열 순서 변경 (이전 열을 참조하여 컬럼을 추가)
일부 데이터베이스에서는 op.add_column() 함수에 insert_before 또는 insert_after를 사용해 컬럼 순서를 지정할 수 있습니다.
def upgrade():
    # `name` 컬럼 앞에 `age` 컬럼 추가
    op.add_column('users', sa.Column('age', sa.Integer), insert_before='name')

def downgrade():
    op.drop_column('users', 'age')

13. SQL 명령어 직접 실행
Alembic에서 제공되지 않는 특정 작업은 op.execute()를 통해 SQL을 직접 실행할 수 있습니다.
def upgrade():
    # SQL 명령어 직접 실행
    op.execute("UPDATE users SET age = age + 1")

def downgrade():
    # 다운그레이드 로직 작성
    op.execute("UPDATE users SET age = age - 1")

14. 인덱스 및 제약조건 이름 지정
제약조건이나 인덱스를 생성할 때 이름을 명시하는 것이 좋습니다.
def upgrade():
    # 제약조건 이름 지정
    op.create_foreign_key('fk_users_role_id', 'users', 'roles', ['role_id'], ['id'])
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
    op.create_check_constraint('ck_users_age', 'users', sa.text('age > 0'))

def downgrade():
    op.drop_constraint('fk_users_role_id', 'users', type_='foreignkey')
    op.drop_constraint('uq_users_email', 'users', type_='unique')
    op.drop_constraint('ck_users_age', 'users', type_='check')
```

---

## 📎 Related

### Technology

- [[alembic|Alembic]] - Alembic 개요 및 Qraft 적용 사례

