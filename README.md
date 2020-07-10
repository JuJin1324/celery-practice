# celery-practice
celery 란? Python 에서 네트워크를 통해서 여러 컴퓨터로 비동기 분산 처리를 도와주는 프레임워크

## Requirements
* Docker Desktop CE
* docker-compose
* python3

## Run
터미널에서 현재 프로젝트로 경로 이동
```bash
cd src
docker-compose up --build
```

### celery startup banner 보기 옵션
tasks.py 파일의 다음 주석 해제
```python
# @after_setup_logger.connect
# def setup_loggers(logger, *args, **kwargs):
#     logger.addHandler(logging.StreamHandler(sys.stdout))
```

### 실행 로그 확인
현재 프로젝트 경로로 새로운 터미널 열기
```bash
# 클라이언트 로그 확인
docker logs celery-client
# Worker 로그 확인
docker logs celery-worker
```

## celery 개념 구성
client -> broker -> worker

### client
Dockerfile: Dockerfile-client  
docker-compose.yml: client  

### broker
Dockerfile: 없음  
docker-compose.yml: mq (a.k.a message queue)    
Redis 사용    

### server(worker)
Dockerfile: Dockerfile-server  
docker-compose.yml: server  


