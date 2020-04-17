## Introduction
오픈마켓 기획, 설계 & API 개발 프로젝트

## 개발 인원 및 기간
- 설계기간 : 2020.03.23 ~ 2020.04.03 (2week)
- 개발기간 : 2020.04.09 ~ 2020.04.17 (2week)
- 개발인원 : 2 Back-End

## 역할 
- 공통부분 : 기획 및 설계와 모델링
- 개발부분 : 로그인/회원가입, 장바구니, 주문, 상품가격 변동(Crontab)

## 적용 기술
- Python
- Django Web Framework
- Bcrypt
- JWT
- Django-crontab
- Django-MPTT
- MySQL
- AWS EC2, RDS
- Gunicorn
- CORS header

## 구현 기능
### 인프라
- Amazon AWS 를 통한 배포
- EC2 인스턴스에 RDS 서버에 설치된 mysql 연동

### 계정
- 판매자 로그인/회원가입
- 구매자 로그인/회원가입
- 이메일 입력 값 검증
- 패스워드 해쉬 및 토큰 발행

### 상품
- 상품 등록
    - 가격 옵션 및 상품 옵션 입력 
- 상품 조회
    - 현재 반영된 할인 가격으로 상품 정보 출력
- 상품 수정

### 장바구니
- 장바구니 담기
- 장바구니 조회

### 주문
- 주문 등록
- 주문 조회


## API Document
[API 문서 보기](https://documenter.getpostman.com/view/10398819/Szf3ZVWN?version=latest#3604e723-d0a9-43b4-85b8-5637deb21109)

## ERD
![데이터모델링](https://raw.githubusercontent.com/Wave1994-Hoon/OpenMarket_Project/master/Database%20ERD.png)
