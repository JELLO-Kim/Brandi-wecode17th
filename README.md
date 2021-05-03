# Brandi Internship

<br>

# 🛠 Backend
- project period : 21.03.15 ~ 21.04.09
- team members : 5 Backend position

<br>

# About project
- 해당 프로젝트는 Service와 Admin 부분 양쪽의 일부 기능을 구현한 프로젝트도 Service는 유저가 확인하는 페이지, Admin은 관리자 혹은 판매자가 확인하는 페이지 입니다.
- Admin은 관리자(이하 master) 와 판매자(이하 seller)의 기능을 구분하여 구현하였습니다.

<br>

# database modeling
- by AqueryTool

![brandi_ERD](https://user-images.githubusercontent.com/71021769/116836236-b7e2be80-ac00-11eb-96d5-ee0962e64b1d.png)



<br>

# 🛠 구현 기능 (check for mine)

## API

**Service**
- [Service] [post] 회원가입&로그인
- [Service] [get] Product list + filtering ✅
- [Service] [get] Product detail + (해당 상품의 Q&A, 판매자의 다른 상품)
- [Service] [post] Product detail에서 Q&A 달기
- [Service] [get, post] 장바구니
- [Service] [get, post] 주문하기
- [Service] [get] Mypage - 주문 내역 ✅
- [Service] [get] Mypage - 주문 상세 내역 ✅
- [Service] [get] Mypage - Q&A 내역 ✅

<br>

**Admin**
- [Admin] [post] seller 회원가입&로그인
- [Admin] [get] [master] seller 계정 목록
- [Admin] [get, patch] [seller] 본인 상세 정보 수정 ✅
- [Admin] [get, patch] [master] seller 한명의 상세 정보 수정 ✅
- [Admin] [patch] [master] seller의 상태 변경
- [Admin] [get] [master] 주문 상세 관리
- [Admin] [path] [master] 주문 상태 변경
- [Admin] [get, post] [seller] 상품 등록

<br>

## AWS
- RDS, EC2 : db 관리
- S3 : 이미지 업로드 관리

<br>

## respone, request 관리
- Error 함수화  ✅
- response 함수화  ✅

<br>

## API document 제작
- postman 을 활용한 API document 제작  ✅
https://documenter.getpostman.com/view/14808954/Tz5wVuBV

<br>

## 이력관리
- 점이력 법을 활용한 이력 관리

<br>

# 🛠 Technologies (Backend)
- language : python 3.9
- framework : flask
- database connetor : pymysql
- database : MySQL
- image upload : boto3
- AWS : RDS, S3
- password hashing : bcrypt
- token : JWT

- Git, CORS
