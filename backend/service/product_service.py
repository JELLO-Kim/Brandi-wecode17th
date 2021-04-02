from model.product_dao import ProductDao
from flask             import jsonify, json
from responses         import *

class ProductService:
    
    def products_category(self, connection):
        products_category_dao = ProductDao()
        products_category = products_category_dao.products_category(connection)

        # 1차 카테고리 항목의 id 값을 parent_id로 갖는 하위 카테고리 항목을 종속 시켜주는 과정
        result = []
        for p in products_category:
            if p['parent_id'] is None:
                p['subCategory'] = []
                for c in products_category:
                    if p['id'] == c['parent_id']:
                        p['subCategory'].append(c)
                result.append(p)

        # null값인 1차 카테고리의 parent_id라는 key 제거
        # for r in result:
        #     r.pop('parent_id')
            
        return {"data" : result}

    def products_list(self, filter_data, connection, page_condition):
        products_dao = ProductDao()
        products_list = products_dao.products_list(filter_data, connection, page_condition)

        return products_list


    
    def get_product_detail(self, product_id, connection):

        """
        제품 상세페이지에서 상품 정보에 관련된 부분 get
        """

        product_dao    = ProductDao()
        product_detail = product_dao.product_detail(product_id, connection)

        if product_detail["imageList"] is not None:
            product_detail["imageList"] = product_detail["imageList"].split(', ')

        """ 제품 구매시 색상 선택 dropbox에 들어갈 내용 포맷 맞추기. {"key": 색상 id, "label": 색상 이름} 형태 """
        if product_detail["colors"] is not None:
            color_group              = [item.split(':') for item in product_detail["colors"].split(',')]
            product_detail["colors"] = [{"key" : int(color[0]), "label" : color[1]} for color in color_group]

        """ 제품 구매시 사이즈 선택 dropbox에 들어갈 내용 포맷 맞추기 {"key": 사이즈 id, "label": 사이즈 이름} 형태 """
        if product_detail["sizes"] is not None:
            size_group               = [item.split(':') for item in product_detail["sizes"].split(',')]
            product_detail["sizes"]  = [{"key" : int(size[0]), "label" : size[1]} for size in size_group]
        
        return {"product" :product_detail}

    
    @user_decorator
    def get_product_qna(self, info, connection):
        
        """
        제품 상세페이지 하단의 질문답변 부분 get: 로그인 유무 상관없이 보여지는 페이지이지만, 로그인 한 경우 작성한 글과 그 글의 답변, 공개글은 공개처리 
        """
        
        product_dao = ProductDao()
        product_qna = product_dao.get_product_question(info, connection)

        """
        비공개 처리되야하는 질문들은 작성자의 아이디도 비공개처리: 아이디 앞 3글자 영문 + *** 로 통일
        질문에 대한 답변자는 항상 seller이고 seller의 브랜드 이름은 질문내용 공개여부 상관없이 항상 브랜드 공개
        """
        for item in product_qna["qna"]:
            if item["parent_id"] is None:
                if item["content"] == "비밀글입니다.":
                    item["username"] = item["username"][:3]+"***" 

        """ 질문에 답변이 있는경우, 질문 객체 안의 답변 객체로 묶어주는 로직 """
        qna_list = []
        for item in product_qna["qna"]:
            tmp = {
                    "id" : item["id"],
                    "questionType" : item["questionType"],
                    "isFinished"   : item["isFinished"],
                    "content"      : item["content"],
                    "writer"       : item["username"],
                    "createdAt"    : item["createdAt"],
                    "isPrivate"    : item["isPrivate"]
                }
            if item["isFinished"] == 1:
                tmp["answer"] = {
                    "content"   : item["r_content"],
                    "writer"    : item["brand"],
                    "createdAt" : item["r_createdAt"]
                }
            qna_list.append(tmp)
    
        return {"data" : qna_list, "totalCount" : product_qna["totalCount"]}


    @login_decorator
    def get_question_open(self, connection):
        """
        로그인 한 회원에 한해서 제품 상세페이지에서 질문 올리는 로직. 질문 올리기 포맷에서 질문타입 선택지 dropdown 내용 
        """

        product_dao   = ProductDao()
        question_open = product_dao.get_question_open(connection)
        type_list     = [{ "key": i["id"], "value": i["name"]} for i in question_open]

        return {'data' : type_list}


    def post_product_qna(self, question_info, connection):

        """
        제품상세페이지 질문 등록
        """

        product_dao = ProductDao()
        post_qna    = product_dao.post_product_qna(question_info, connection)

        return post_qna


    def get_other_products(self, info, connection):

        """ 
        제품 상세페이지 하단, 판매자의 다른상품 추천 로직: 현재 조회중인 상품을 제외한 판매자의 다른 상품 5개 랜덤 추천
        """

        product_dao   = ProductDao()
        products_list = product_dao.get_other_products(info, connection)

        return {'data' : products_list}
