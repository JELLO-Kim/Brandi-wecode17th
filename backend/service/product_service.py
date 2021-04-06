from model.product_dao import ProductDao
from flask          import jsonify, json
from responses         import *

class ProductService:
    
    def products_category(self, connection):
        """ [서비스] products의 category list
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
        Returns: 
            - 200: { "data" : category list,
                     "totalCount" : 2차 카테고리 총 갯수
                    }
        """
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
            
        return {"data" : result}

    def products_list(self, connection, page_condition):
        """ [서비스] products list
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - page_condition : limt, offset, filtering용 category 조건
        Returns: 
            - 200 : {
                    "data" : product list,
                    "totalCount" : 상품의 총 갯수
                    }
        """
        products_dao        = ProductDao()
        products_list       = products_dao.products_list(connection, page_condition)
        product_total_count = products_dao.product_list_total_count(connection, page_condition)
        print('????????????/', product_total_count)

        return {"data" : products_list, "totalCount" : product_total_count['COUNT(*)']}


    def get_product_detail(self, product_id, connection):
        product_dao    = ProductDao()
        product_detail = product_dao.product_detail(product_id, connection)

        if product_detail["imageList"] is not None:
            product_detail["imageList"] = product_detail["imageList"].split(', ')
        else:
            product_detail["imageList"] = 0

        if product_detail["colors"] is not None:
            color_group              = [item.split(':') for item in product_detail["colors"].split(',')]
            product_detail["colors"] = [{"key" : int(color[0]), "label" : color[1]} for color in color_group]

        if product_detail["sizes"] is not None:
            size_group               = [item.split(':') for item in product_detail["sizes"].split(',')]
            product_detail["sizes"]  = [{"key" : int(size[0]), "label" : size[1]} for size in size_group]
        return {"product" :product_detail}


    def get_product_qna(self, info, connection):
        product_dao = ProductDao()
        product_qna = product_dao.get_product_question(info, connection)

        for item in product_qna["qna"]:
            if item["parent_id"] is None:
                if item["contents"] == "비밀글입니다.":
                    item["username"] = item["username"][:3]+"***" 

        qna_list = []
        for item in product_qna["qna"]:
            tmp = {
                    "id" : item["id"],
                    "questionType" : item["questionType"],
                    "isFinished"   : item["isFinished"],
                    "contents"     : item["contents"],
                    "writer"       : item["username"],
                    "createdAt"    : item["createdAt"],
                    "isPrivate"    : item["isPrivate"]
                }
            if item["isFinished"] == 1:
                tmp["answer"] = {
                    "contents"   : item["r_contents"],
                    "writer"    : item["brand"],
                    "createdAt" : item["r_createdAt"]
                }
            qna_list.append(tmp)
    
        return {"data" : qna_list, "totalCount" : product_qna["totalCount"]}


    def get_question_open(self, connection):
        product_dao   = ProductDao()
        question_open = product_dao.get_question_open(connection)
        type_list     = [{ "key": i["id"], "value": i["name"]} for i in question_open]

        return {'data' : type_list}


    def post_product_qna(self, question_info, connection):
        product_dao = ProductDao()
        post_qna_id = product_dao.post_product_qna(question_info, connection)

        log_info = {
            "user_id" : question_info["user_id"],
            "qna_id" : post_qna_id
        }
        post_qna_log_id = product_dao.post_product_qna_log(log_info, connection)
        
        return {"qna_id": post_qna_id, "qna_log_id": post_qna_log_id}


    def get_other_products(self, info, connection):
        product_dao   = ProductDao()
        products_list = product_dao.get_other_products(info, connection)

        return {'data' : products_list}
