# Flask + Nginx + Docker + S3 프로젝트 배포 구성

## 프로젝트 개요

Flask 애플리케이션을 AWS EC2 서버에 Docker를 활용하여 배포하고, 정적 파일 저장은 AWS S3를 이용하는 구조
Nginx를 리버스 프록시 서버로 사용하여 웹/애플리케이션 서버를 분리해 운영 환경을 구성

---

## 인프라 구성도

```
사용자
 |
 | HTTP 요청
 v
Nginx (EC2 내부)
 |  - / : 정적 자산 (HTML, CSS, JS)
 |  - /upload : Flask API 서버로 요청 전달
 |
Docker Compose
 |- Flask API 서버 (uWSGI 기반)
 |- Nginx Reverse Proxy

AWS S3 : 정적 파일 (이미지 등) 저장
```

---

## 사용 스택

### 백엔드
- Python 3.10
- Flask
- uWSGI

### 인프라
- AWS EC2 (Ubuntu)
- AWS S3  
- Docker
- Docker Compose
- Nginx

---

## 프로젝트 폴더 구조

```
project/
├── app/              # Flask 애플리케이션
│   ├── main.py       
│   ├── config.py
│   ├── requirements.txt
│   ├── s3_upload.py  # S3 업로드 모듈
│   └── s3_download.py
├── nginx/            # Nginx 설정 파일
│   └── default.conf
├── .env              # AWS Key, Flask Secret Key
├── Dockerfile        # Flask + uWSGI
├── docker-compose.yml
└── README.md
```

---

## 주요 기능

### 1. S3 파일 업로드 API

```
POST /upload
Body : Multipart Form (file)
Response : S3 저장된 파일 이름
```

### 2. S3 파일 다운로드 URL 반환 API

```
GET /image/<filename>
Response : S3 URL 반환
```

---

## EC2 서버 배포 과정

### 1. EC2 서버 준비

```bash
sudo apt-get update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose
```

### 2. .env 파일 설정

```
FLASK_SECRET_KEY=your_secret_key
AWS_ACCESS_KEY=your_aws_key
AWS_SECRET_KEY=your_aws_secret_key
BUCKET_NAME=your_bucket_name
REGION=ap-northeast-2
```

### 3. Docker Build & Run

```bash
sudo docker-compose up -d --build
```

---

## Nginx 설정 (리버스 프록시)

```
server {
    listen 80;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## S3 버킷 정책 (정적 파일 퍼블릭 접근 허용)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your_bucket_name/*"
    }
  ]
}
```

---

## 테스트 방법

### 파일 업로드

Postman에서:
```
POST http://<EC2_IP>/upload
Form-Data : file 업로드
```

### 이미지 조회
```
GET http://<EC2_IP>/image/<filename>
```
반환된 URL로 브라우저에서 접근

---

## 결과 예시

- API 서버 정상 동작
- 이미지 S3 업로드 및 조회 성공
- Nginx 리버스 프록시 설정 완료
- Docker Compose 기반 서비스 구성 완료

## jenkins test
