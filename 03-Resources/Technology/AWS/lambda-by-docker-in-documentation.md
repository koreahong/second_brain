---
title: lambda by docker in documentation
type: resource
tags:
- ECR
- Lambda
- aws
---

## 개념

- lambda를 ECR기반으로 생성하는 부분
## 목적

- ECR로 버전관리를 하기 위한 목적
## 서칭내용

- documentation에서 제시한 예제 코드
  ```bash
  FROM public.ecr.aws/lambda/python:3.8
  
  # Copy function code
  COPY app.py ${LAMBDA_TASK_ROOT} 
  COPY requirements.txt  ${LAMBDA_TASK_ROOT} 
  
  # install dependencies
  RUN pip3 install --user -r requirements.txt
  
  # Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
  CMD [ "app.lambda_handler" ]
  ```

1. aws에서 lambda에 python을 사용할 수 있게 image를 배포함
  ```bash
  FROM public.ecr.aws/lambda/python:3.8
  COPY app.py ${LAMBDA_TASK_ROOT} 
  COPY requirements.txt  ${LAMBDA_TASK_ROOT} 
  ```

  해당 이미지를 사용하면, entrypoint, 환경변수 등이

  AWS 권고사항에 맞게 미리 세팅이 되어 있어서 사용하기 편리함

1. lambda가 생성되면 작동하는 코드
  ```bash
  CMD [ "app.lambda_handler" ]
  ```

  workdir에 있는 app.py에 lambda_handler 함수를 실행한다는 뜻