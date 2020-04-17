## Introduction
오픈마켓 기획, 설계 & API 개발 프로젝트

## 개발 인원 및 기간
- 설계기간 : 2020.03.23 ~ 2020.04.03
- 개발기간 : 2020.04.09 ~ 2020.04.17 (2week)
- 개발인원 : 2 Back-End

## 적용 기술
- Python
- Django Web Framework
- Google SMTP
- Bcrypt
- JWT
- MySQL
- AWS EC2, RDS
- Gunicorn
- CORS header

## 구현 기능
### 인프라
- Amazon AWS 를 통한 배포
- EC2 인스턴스에 RDS 서버에 설치된 mysql 연동

### 계정
- 로그인 / 회원가입
- 이메일 / 패스워드 입력 값 검증
- 이메일 인증 (Google SMTP)
- 패스워드 해쉬 및 토큰 발행
- 고객 자산 조회

### 상품
- 매수/매도 기능
- 주문 내역 조회
- 거래 완료 내역 조회
- 24h Volume, 고가, 저가, 현재 가격 조회
- 코인 리스트 조회
- 차트 작성을 위한 과거 데이터 조회

## API Document
[API 문서 보기](https://documenter.getpostman.com/view/10398819/SzS8s59w?version=latest)

## ERD
![데이터모델링](https://k.kakaocdn.net/dn/zBxIC/btqDf02CwaQ/rCG8klfkzKwOo6C0ZHKJKk/img.png)

