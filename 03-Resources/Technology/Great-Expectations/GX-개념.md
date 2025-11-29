---
title: GX 개념
type: resource
tags:
- GX
---

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/f1611d33-0e9c-4f04-b79f-d54dc8b307ba/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4667EOE7VL5%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T021210Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIGuaoVL2RHKPFYae1zsDl1JbEtMJ9bG46iI1JwN2nuHjAiEA8lMgcrGRPjsDM1QB4PPiH%2FX0DC%2BIDspYNhm9GJNLrHgqiAQIwf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDJct%2Bj5YeX6AGnTp7CrcA13ClRIwcVX2f36aRPePjuFTPBykxbiFWwjClEGPQS6PLzYvVDsBAxxkGCHhcDtmuN8tKKT7yfCDbFH74GKsBNVdgFc7EMuKUmrzedpHRR7nWbwtXkg0iQkkoOuu393gEF3IDw5Y0WNHzQn%2FRFUQULzSvsdlWp7vjjxSBKGzz9QRqWJXzQqY%2BjRQjhR7eZ2RVRF76z8E%2F01TvZlaubVxHHbE2L5syzKeSJvtFilOHP9LWHMT%2Fv6Y8AFvlCHJig6g9VVCiFTFk%2BlKuSpYEQ67uUpzMyw%2FSXMaAgvqSgqh1IMPIplkb5SbWTWtslDMjXYqb0GAkY%2FGmPyYxcggK5TjxcM6OIgLs9ssELFRlvPJ4RqONzHA5GniwsqbtFuxRGjlt5q7VipdB9o5Q1x5SSRTgbeJZ9pYz8VUnCPGadPlnlObBqD7%2FkNJip5Ks0tlVCMiBf2fE0ajSTPBHKbcq%2BzxPZLwVvXYdgpt5PiCVvjQhNiVNFLsIeTdGbyIy%2B%2BkipIrFe5LSfWPdAGrd4llsL4J9LFfX3OO0XaJWakI7jSq6Sh00hOTYp%2ByRbFo1VCetSBR7gdnNE25pm2HAES%2FiOBCN%2BS3cOK1ZYkp%2B6kwnTA2q7o9D5lGxzdryn4cvCMLMMz5qMkGOqUB71WALo2Qo5qAndrs7S4sPibAKXORpU7jzkcHavx%2BdRJkX9hi21nBEFS3noY9IlE6bf1IF5dpUaHOKgU3fpaIDKBSo%2F6CmVxDh6L6atKIhh5kDZLRb2%2BhNptUPUpRfBy06bb2mZiXYq4h7udey80w3DRKbyf53L%2BNklF%2F28dcb5Af%2FCB%2BILk48Ge8dfbRsXZBgFej7iNYoEzkPd7ePRhMkbwFopfM&X-Amz-Signature=6ce47f29991ec1029a96f18aedda54f2aa7c55feedff0729856b66ca97464b83&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- GX는 크게 4가지 workflow로 구성됨
  - 환경세팅
  - data 연결
  - expectations 정의(데이터품질 기준)
  - 검증
- 환경세팅
  - context 설정
  - workflow에서 참고하는 정보
  - workflow를 구분하는 단위
context는 검증의 일련의 단계를 구분하는 gx 최상위 단위임

data source는 검증할 데이터를 구분을 짓기 위한 단위

data asset은 실제 data가 저장되는 단위

batch definition은 data asset을 특정한 컬럼의 값과 같은 기준을 갖고 batch로 나눈 것

expectation은 각 컬럼별로 검증해야 할 내용들을 정의한 것

Validation Definition은 expectation에서 정의한 기댓값들을 검증하는 단위