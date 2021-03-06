# Brandi Internship

<br>

# π  Backend
- project period : 21.03.15 ~ 21.04.09
- team members : 5 Backend position

<br>

# About project
- ν΄λΉ νλ‘μ νΈλ Serviceμ Admin λΆλΆ μμͺ½μ μΌλΆ κΈ°λ₯μ κ΅¬νν νλ‘μ νΈλ Serviceλ μ μ κ° νμΈνλ νμ΄μ§, Adminμ κ΄λ¦¬μ νΉμ νλ§€μκ° νμΈνλ νμ΄μ§ μλλ€.
- Adminμ κ΄λ¦¬μ(μ΄ν master) μ νλ§€μ(μ΄ν seller)μ κΈ°λ₯μ κ΅¬λΆνμ¬ κ΅¬ννμμ΅λλ€.

<br>

# Project tree
```bash
.
βββ README.md
βββ __pycache__
βββ app.py
βββ config.py
βββ db_connector.py
βββ model
βΒ Β  βββ __init__.py
βΒ Β  βββ __pycache__
βΒ Β  βΒ Β  βββ __init__.cpython-39.pyc
βΒ Β  βββ master_dao.py
βΒ Β  βββ mypage_dao.py
βΒ Β  βββ order_dao.py
βΒ Β  βββ product_dao.py
βΒ Β  βββ seller_dao.py
βΒ Β  βββ user_dao.py
βββ requirements.txt
βββ responses.py
βββ run.py
βββ service
βΒ Β  βββ __init__.py
βΒ Β  βββ __pycache__
βΒ Β  βΒ Β  βββ __init__.cpython-39.pyc
βΒ Β  βββ ch_test.py
βΒ Β  βββ master_service.py
βΒ Β  βββ mypage_service.py
βΒ Β  βββ order_service.py
βΒ Β  βββ product_service.py
βΒ Β  βββ seller_service.py
βΒ Β  βββ user_service.py
βββ utils.py
βββ validators.py
βββ view
    βββ __init__.py
    βββ __pycache__
    βΒ Β  βββ __init__.cpython-39.pyc
    βββ master_view.py
    βββ mypage_view.py
    βββ order_view.py
    βββ product_view.py
    βββ seller_view.py
    βββ service_view.py
    βββ user_view.py
```

# database modeling
- by AqueryTool

![brandi_ERD](https://user-images.githubusercontent.com/71021769/116836236-b7e2be80-ac00-11eb-96d5-ee0962e64b1d.png)



<br>

# π  κ΅¬ν κΈ°λ₯ (check for mine)

## API

**Service**
- [Service] [post] νμκ°μ&λ‘κ·ΈμΈ
- [Service] [get] Product list + filtering β
- [Service] [get] Product detail + (ν΄λΉ μνμ Q&A, νλ§€μμ λ€λ₯Έ μν)
- [Service] [post] Product detailμμ Q&A λ¬κΈ°
- [Service] [get, post] μ₯λ°κ΅¬λ
- [Service] [get, post] μ£Όλ¬ΈνκΈ°
- [Service] [get] Mypage - μ£Όλ¬Έ λ΄μ­ β
- [Service] [get] Mypage - μ£Όλ¬Έ μμΈ λ΄μ­ β
- [Service] [get] Mypage - Q&A λ΄μ­ β

<br>

**Admin**
- [Admin] [post] seller νμκ°μ&λ‘κ·ΈμΈ
- [Admin] [get] [master] seller κ³μ  λͺ©λ‘
- [Admin] [get, patch] [seller] λ³ΈμΈ μμΈ μ λ³΄ μμ  β
- [Admin] [get, patch] [master] seller νλͺμ μμΈ μ λ³΄ μμ  β
- [Admin] [patch] [master] sellerμ μν λ³κ²½
- [Admin] [get] [master] μ£Όλ¬Έ μμΈ κ΄λ¦¬
- [Admin] [path] [master] μ£Όλ¬Έ μν λ³κ²½
- [Admin] [get, post] [seller] μν λ±λ‘

<br>

## AWS
- RDS, EC2 : db κ΄λ¦¬
- S3 : μ΄λ―Έμ§ μλ‘λ κ΄λ¦¬

<br>

## respone, request κ΄λ¦¬
- Error ν¨μν  β
- response ν¨μν  β

<br>

## API document μ μ
- postman μ νμ©ν API document μ μ  β
https://documenter.getpostman.com/view/14808954/Tz5wVuBV

<br>

## μ΄λ ₯κ΄λ¦¬
- μ μ΄λ ₯ λ²μ νμ©ν μ΄λ ₯ κ΄λ¦¬

<br>

# π  Technologies (Backend)
- language : python 3.9
- framework : flask
- database connetor : pymysql
- database : MySQL
- DB connector : pymysql
- image upload : AWS(S3)
- AWS : RDS, EC2
- password hashing : bcrypt
- token : JWT

- Git, CORS
