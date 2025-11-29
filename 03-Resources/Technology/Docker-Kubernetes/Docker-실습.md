---
title: Docker 실습
type: resource
tags:
- docker
---

```shell

-- 도커 다운로드
sudo wget -qO- <http://get.docker.com/> | sh

sudo apt install containerd #ubuntu 버전 맞추기

sudo apt-get install docker.io

-- cadivsor 컨테이너
이미지가 있으면, 이미지를 통해 컨테이너 생성할 수 잇음, google/cadvisor:latest -> 이미지 -> 컨테이너 실행
sudo docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --vo
lume=/sys/:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=9559:8080 --detach=true -
-name=cadvisor google/cadvisor:latest

-- nginx 컨테이너
sudo docker pull nginx:1.18

sudo docker run --name webserver1 -d -p 80:80 nginx:1.18

-- 도커 컨테이너 실행관련 명령어
docker stop -> sigkill을 날려서 프로세스를 정지하는 것

docker pause -> sigstop
docker unpause

-- python 컨테이너
 sudo docker run -it -d --name=python_test -p 8900:8900 python
sudo docker cp ./py_lotto.py python_test:/
sudo docker exec -it python_test python /py_lotto.py
sudo docker exec -it python_test python /py_lotto.py

-- 이미지생성
컨테이너를 이미지로 저장하고, nub에 이미지를 저장한다
docker commit -a(author) 컨테이너이름 tag
sudo docker commit -a "batteryker" python_test python_test:1.0

-- volume 생성
sudo docker volume create my-appvol-1

```

#docker-cgroup

### 컨테이너 데이터 저장

### volume / bind mount

- docker에 돌아가는 많은 컨테이너의 생명 주기와 관계없이 데이터를 영속적으로 저장하기 위한 장치, 또한 컨테이너끼리 데이터를 공유할 수 있는 하나의 저장공간 장치
volumn운 따로 저장소를 만드는 것이고 마운트는 호스트 디렉토리와 연결하는 것이다.