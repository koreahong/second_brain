---
title: TypeB CRM 서비스 구축
created: 2024-06-10
tags: ["reference", "migrated", "project", "\uc5c5\ubb34"]
PARA: Project
구분: ["\uc5c5\ubb34"]
---

# TypeB CRM 서비스 구축

## 📝 내용

컨텐츠, 개인정보처리, 실험설계

```javascript
Host dev-bastion
	Hostname 3.39.80.79
	User ubuntu
	IdentityFile ~/.ssh/aice_bastion.pem

Host dev-api
	Hostname 10.0.0.198
	User ubuntu
	IdentityFile ~/.ssh/aice-backend.pem
    ProxyCommand ssh dev-bastion -W %h:%p #dev-bastion은 위에서 정의한 dev-bastion의 호스트명입니다.

Host aice-dev-airflow-main
	Hostname 10.0.0.201
	User ubuntu
	IdentityFile ~/.ssh/aice-data.pem
    ProxyCommand ssh dev-bastion -W %h:%p #dev-bastion은 위에서 정의한 dev-bastion의 호스트명입니다.

Host aive-dev-airflow-worker-1
	Hostname 10.0.0.199
	User ubuntu
	IdentityFile ~/.ssh/aice-data.pem
    ProxyCommand ssh dev-bastion -W %h:%p #dev-bastion은 위에서 정의한 dev-bastion의 호스트명입니다.

Host aive-dev-airflow-worker-2
	Hostname 10.0.0.196
	User ubuntu
	IdentityFile ~/.ssh/aice-data.pem
    ProxyCommand ssh dev-bastion -W %h:%p #dev-bastion은 위에서 정의한 dev-bastion의 호스트명입니다.


```

## 🏷️ 분류

- **PARA**: Project
- **구분**: 업무

## 🔗 연결

**Hub**: [[_HUB_Data_Engineering]], [[_HUB_Analytics]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
