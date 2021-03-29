from model.product_dao import ProductDao
from flask          import jsonify, json
from errors         import *

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
