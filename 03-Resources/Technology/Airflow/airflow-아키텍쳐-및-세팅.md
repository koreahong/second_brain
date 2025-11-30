---
title: airflow 아키텍쳐 및 세팅
type: resource
tags:
  - airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

# 레퍼런스

---

https://tech.socarcorp.kr/data/2021/06/01/data-engineering-with-airflow.html

https://tech.socarcorp.kr/data/2022/11/09/advanced-airflow-for-databiz.html

https://blog.doctor-cha.com/buliding-local-airflow-and-apply-vault

https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-1

https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-2

https://amazelimi.tistory.com/entry/Airflow-KubernetesExecutor-vs-CeleryExecutor-LIM

https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html

https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html

https://happycloud-lee.tistory.com/3

https://velog.io/@sms8377/Celery-Python-Celery란

https://velog.io/@wnguswn7/Redis란-무엇일까-Redis의-특징과-사용-시-주의점

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/1a4747e1-49c2-4684-84ed-0671773e368c/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664CQKM2H6%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015544Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBtPooZWOyGDyfbwxd94BJifYbVKyz1EhsbywwIY9ylbAiAIGmXfeCL3FQqp7f4QdWEthhzgHFgjhn%2BUgy%2B0IUznLyqIBAjC%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMpV48R4c8TiU9PoBvKtwDAnunozPYhG11e1qgd%2BRompeK3ukJpmDJNIn%2FTyH56O8tjoUVq2xayuTPHPxxhBL3Vwi3vYFJHnbcHh%2BePEZzJ3%2B%2FsMWnKtxoyHQsaltfHrMVESQPUYsyZj7pAUJbOYRl93EBF0IwQrVhNucCqwMTPUgFdUFlWUkmcEwAEG9kN%2BeUiBZK5T%2F7aMTu3PpOfCL8uNIe8sjB2CTR1BFi2y1m1YQnQOxB164WHYnoZKdnKEUgShHT0GxxE23fYREfQGExzfJKE85b4TiqfhV%2FL44JnUeo6F3oCFqwavIu8JettjS5iYhJkmvmJjL4kVx2Ii1HqvUULZgQUBIEleQVXoqeDVsU6TJyhEcFgasviA2mWTAZ1ULmjolFLhBqHReIddU60zheiuZmDGHIK6oThHDBDV9CwZe9lllccfBJsS2t14YQ7SS1l%2BHor9miDsNbye9fOQakx9cHaPLGOCXSwY%2FQdvktFxvGF2URSs0wt9Xd6ij%2BntNLVZLIY9Aw6g3aPBO8SO%2BjqsKLob2V3ahdR%2BEKSCpVSuFIulZs2MiC5UCANqs2wBg11A7FQkZqwnSfwIJF3nazn2JlNTLJ3sdd2L23GPcOsSkwEFkify02a67KyLrknReg%2FKbgKM9tJRUw3vyoyQY6pgGaf2N0B348IsR2SVjRqJIlR9JrltZeEfw3VZno5BVRLoUJLajNEtfeoQUKvtx4N1lSDKP0c4e9ofaxiI6AUAxqKsMNr%2Bp4Ajmw9GG0uqc7SfeLNzgFf13saUH8VQGaIY%2B0mJd%2BZyTO2QKOszA5VSQ4A80%2BRjW1ISSnpeLvx90tJq4ltpBu4UN%2BmRLPUXsi0cstYzucG1%2BDHiW1k8%2BPWfVylyKsliqr&X-Amz-Signature=448c1e20b05b670597867b6ba21eed98ea82cef73d7b6846350ccbcc66e7fb67&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

# 내용

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/7624a06f-da08-400f-989a-cabd0fe1b651/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664CQKM2H6%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015544Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBtPooZWOyGDyfbwxd94BJifYbVKyz1EhsbywwIY9ylbAiAIGmXfeCL3FQqp7f4QdWEthhzgHFgjhn%2BUgy%2B0IUznLyqIBAjC%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMpV48R4c8TiU9PoBvKtwDAnunozPYhG11e1qgd%2BRompeK3ukJpmDJNIn%2FTyH56O8tjoUVq2xayuTPHPxxhBL3Vwi3vYFJHnbcHh%2BePEZzJ3%2B%2FsMWnKtxoyHQsaltfHrMVESQPUYsyZj7pAUJbOYRl93EBF0IwQrVhNucCqwMTPUgFdUFlWUkmcEwAEG9kN%2BeUiBZK5T%2F7aMTu3PpOfCL8uNIe8sjB2CTR1BFi2y1m1YQnQOxB164WHYnoZKdnKEUgShHT0GxxE23fYREfQGExzfJKE85b4TiqfhV%2FL44JnUeo6F3oCFqwavIu8JettjS5iYhJkmvmJjL4kVx2Ii1HqvUULZgQUBIEleQVXoqeDVsU6TJyhEcFgasviA2mWTAZ1ULmjolFLhBqHReIddU60zheiuZmDGHIK6oThHDBDV9CwZe9lllccfBJsS2t14YQ7SS1l%2BHor9miDsNbye9fOQakx9cHaPLGOCXSwY%2FQdvktFxvGF2URSs0wt9Xd6ij%2BntNLVZLIY9Aw6g3aPBO8SO%2BjqsKLob2V3ahdR%2BEKSCpVSuFIulZs2MiC5UCANqs2wBg11A7FQkZqwnSfwIJF3nazn2JlNTLJ3sdd2L23GPcOsSkwEFkify02a67KyLrknReg%2FKbgKM9tJRUw3vyoyQY6pgGaf2N0B348IsR2SVjRqJIlR9JrltZeEfw3VZno5BVRLoUJLajNEtfeoQUKvtx4N1lSDKP0c4e9ofaxiI6AUAxqKsMNr%2Bp4Ajmw9GG0uqc7SfeLNzgFf13saUH8VQGaIY%2B0mJd%2BZyTO2QKOszA5VSQ4A80%2BRjW1ISSnpeLvx90tJq4ltpBu4UN%2BmRLPUXsi0cstYzucG1%2BDHiW1k8%2BPWfVylyKsliqr&X-Amz-Signature=74d88a4c198fee37eaf5ad31a5d3bd9d06f9622f0ee0f9a07ac8e6a215eeb4eb&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/75cee7ce-955c-4d33-bb1f-b4b95ea48b87/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664CQKM2H6%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015544Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBtPooZWOyGDyfbwxd94BJifYbVKyz1EhsbywwIY9ylbAiAIGmXfeCL3FQqp7f4QdWEthhzgHFgjhn%2BUgy%2B0IUznLyqIBAjC%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMpV48R4c8TiU9PoBvKtwDAnunozPYhG11e1qgd%2BRompeK3ukJpmDJNIn%2FTyH56O8tjoUVq2xayuTPHPxxhBL3Vwi3vYFJHnbcHh%2BePEZzJ3%2B%2FsMWnKtxoyHQsaltfHrMVESQPUYsyZj7pAUJbOYRl93EBF0IwQrVhNucCqwMTPUgFdUFlWUkmcEwAEG9kN%2BeUiBZK5T%2F7aMTu3PpOfCL8uNIe8sjB2CTR1BFi2y1m1YQnQOxB164WHYnoZKdnKEUgShHT0GxxE23fYREfQGExzfJKE85b4TiqfhV%2FL44JnUeo6F3oCFqwavIu8JettjS5iYhJkmvmJjL4kVx2Ii1HqvUULZgQUBIEleQVXoqeDVsU6TJyhEcFgasviA2mWTAZ1ULmjolFLhBqHReIddU60zheiuZmDGHIK6oThHDBDV9CwZe9lllccfBJsS2t14YQ7SS1l%2BHor9miDsNbye9fOQakx9cHaPLGOCXSwY%2FQdvktFxvGF2URSs0wt9Xd6ij%2BntNLVZLIY9Aw6g3aPBO8SO%2BjqsKLob2V3ahdR%2BEKSCpVSuFIulZs2MiC5UCANqs2wBg11A7FQkZqwnSfwIJF3nazn2JlNTLJ3sdd2L23GPcOsSkwEFkify02a67KyLrknReg%2FKbgKM9tJRUw3vyoyQY6pgGaf2N0B348IsR2SVjRqJIlR9JrltZeEfw3VZno5BVRLoUJLajNEtfeoQUKvtx4N1lSDKP0c4e9ofaxiI6AUAxqKsMNr%2Bp4Ajmw9GG0uqc7SfeLNzgFf13saUH8VQGaIY%2B0mJd%2BZyTO2QKOszA5VSQ4A80%2BRjW1ISSnpeLvx90tJq4ltpBu4UN%2BmRLPUXsi0cstYzucG1%2BDHiW1k8%2BPWfVylyKsliqr&X-Amz-Signature=994c5c4fd6f962b043e73344554bdd8489d1af2f331f777b1efe26eac42aeec0&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

구조는 거의 비슷하지만 worker는 항상 리소스를 점유하지 않는다. airflow가 스케쥴링된 DAG를 실행하기 위해는 쿠버네티스에게 worker pod 생성을 요청한다. (이때 pod의 리소스를 제한 할 수도 있다.)이후 생성한 pod(worker)에 task를 할당하고, task를 완료한 후에는 리소스를 다시 반납한다. 즉 유동적으로 리소스를 사용할 수 있다.

Airflow는 실시간 처리가 아닌 배치 처리를 위한 workflow engine이고 그렇기 때문에 분명 스케쥴이 돌지 않는 시간이 존재한다. 대부분의 운영 환경에서 DAG Job이 도는 시간 보다는 Idle 상태로 worker가 리소스를 점유하고 있는 시간이 더 길 것이라고 생각한다.

쿠버네티스 executor는 동적으로 worker pod를 생성해서 task를 실행한다. 그런데 여기서 라이브러리 종속성 문제가 발생하게 된다. 하나의 쿠버네티스 클러스터 내에서 하나의 에어플로우를 운영할 때 Spark2, 3 버전을 둘 다 사용해야 하는 경우를 예로 들 수 있다.

Helm은 컨테이너를 쉽게 설치할 수 있도록 돕는 툴

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

