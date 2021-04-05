from model.mypage_dao   import MyPageDao
from flask              import jsonify, json
from responses             import *

class MyPageService:

    def mypage_qna(self, connection, user_id, page_condition):
        """ [서비스] 로그인 유저의 mypage - qna list
        Author : Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
            page_condition : limit, offset, filtering 조건에 필요한 answer에 대한 값
        Returns 
            : {
                "data" : 로그인 유저의 질문 list,
                "totalCount" : 질문 총 갯수
                }
        """
        mypage_dao = MyPageDao()
        mypage_qna = mypage_dao.mypyage_qna_dao(connection, user_id, page_condition, answer)
        #totalCount 수 반환
        mypage_count = mypage_dao.mypage_qna_count(connection, user_id, answer)[0]
        total_count = mypage_count['COUNT(*)']

        result = []
        for row in mypage_qna:
            question = {
                'id'            : row['id'],
                'username'      : row['username'],
                'contents'      : row['contents'],
                'category'      : row['category'],
                'createdAt'     : row['created_at'],
                'isFinished'    : row['isFinished']
            }
            # 답변이 있는경우 answer에 담아줌
            if row['answer_id']:
                question['answer'] = {
                    'id'        : row['answer_id'],
                    'replier'   : row['answer_replier'],
                    'contents'  : row['answer_contents'],
                    'createdAt' : row['answer_time'],
                    'parentId'  : row['answer_parent']
                }
            result.append(question)
        return {"data" : result, "totalCount" : total_count}

    def mypage_order(self, connection, user_id, page_condition):
        """ [서비스] 로그인 유저의 mypage - order list
        Author : Chae hyun Kim
        Args :
            connection : 커넥션
            user_id : 로그인 유저의 user_id
            page_condition : limit, offset에 대한 값
        Returns 
            : {
                "data" : 로그인 유저의 주문내역 list,
                "totalCount" : 주문내역 총 갯수 (하나의 주문번호당 한 개 취급)
                }
        """
        mypage_dao = MyPageDao()
        #totalCount수 반환
        order_count = mypage_dao.mypage_order_count(connection, user_id)[0]
        total_count = order_count['COUNT(*)']

        # 로그인 유저의 주문 목록 반환
        print('service에서 보는 user_id', user_id)
        order_header = mypage_dao.mypage_order_header_dao(connection, user_id, page_condition)
        print('order_header', order_header)
        order_id = [o['id'] for o in order_header]
        
        # 해당되는 주문목록에 속하는 구매 목록 반환
        order_cart = mypage_dao.mypage_order_cart_dao(connection, user_id, page_condition, order_id)
        order_list = [{
            "orderId" : order_head['id'],
            "orderNumber" : order_head['orderNumber'],
            "orderTime" : order_head['created_at'],
            'product': []
        } for order_head in order_header]

        for cart in order_cart:
            order_num = cart['orderNumber']
            brand = cart['brand']
            order = list(filter(lambda d: d['orderNumber'] == order_num,  order_list))[0]
            option_brand = list(filter(lambda d: d['brand'] == brand,  order['product']))
            if not option_brand:
                option_brand = {'brand': brand, 'option':[]}
                order['product'].append(option_brand)
            else:
                option_brand = option_brand[0]
            option_brand['option'].append(cart)

        return {"data" : order_list, "totalCount" : total_count}

    # 상세 주문내역 (로그인 유저의 주문번호 1건에 대한 내용)
    def mypage_order_detail(self, connection, user_id, order_id):
        """ [서비스] 로그인 유저의 mypage - order list
        Author : Chae hyun Kim
        Args :
            connection : 커넥션
            user_id : 로그인 유저의 user_id
            order_id : 상세로 확인할 주문내역의 pk값 (id)
        Returns 
            : {
                "data" : 상세로 확인할 주문내역에 대한 정보,
                "shipping" : 상세주문건에 해당되는 배송지에 대한 정보,
                "totalCount" : 상세 주문내역에 해당하는 각 상품 옵션의 갯수
                }
        """
        mypage_dao = MyPageDao()
        mypage_order_detail= mypage_dao.mypage_order_detail_header_dao(connection, user_id, order_id)
        products_list = mypage_order_detail['detailProducts']
        order = mypage_order_detail['detailHeader']
        brand_name = []

        # 중복 없이 한건의 주문내역에 포함되는 판매 브랜드 이름 배열
        for one_brand in products_list:
            brand_name.append(one_brand['brand'])
        brand_name_one = list(set(brand_name))

        order_dict = {
            "orderId"       : order['id'],
            "orderNum"      : order['order_number'],
            "orderTime"     : order['created_at'],
            "orderName"     : order['order_name'], #username말고 order_name으로 바뀔것
            "discountPrice" : order['total_price'],
            "product"       : 
                [{
                    "brand" : one
                } for one in brand_name_one]
        }
        # 같은 브랜드의 상품을 배열 안에 묶어주는 로직
        for one_brand_name in order_dict['product']:
            brand = one_brand_name['brand']
            product_options = list(filter(lambda x:x['brand'] == brand, products_list))
            one_brand_name['option'] = product_options
        
        #주문 한건에  포함되는 모든 상품옵션 내역 갯수 반환
        total_count = mypage_dao.order_detail_cart_count(connection, order_id)

        #해당 주문건의 배송정보 반환
        detail_shipping = mypage_dao.detail_shipping_info(connection, order_id)
 
        return {"data" : order_dict, "shipping" : detail_shipping, "totalCount" : total_count['COUNT(*)']}
