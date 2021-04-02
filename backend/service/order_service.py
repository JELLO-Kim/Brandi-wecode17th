from model.order_dao import OrderDao
from flask           import jsonify, json
from responses       import *
from datetime        import date, datetime


class ProductService:

    @login_decorator
    def get_address(self, user_id, connection):

        """
        이전 배송지 목록 가져오기
        """

        order_dao   = OrderDao()
        get_address = order_dao.get_address(user_id, connection)

        return {'data': get_address}


    def post_address(self, address_info, connection):
        
        """
        배송지 신규 등록
        """
        
        order_dao   = OrderDao()
        post_address = order_dao.post_address(user_id, connection)

        return {'data': post_address}


    def post_order_confirm(self, order_info, connection):
        
        """
        order table에서 status=1로 장바구니 상태인 상품들 중 결제 된 상품들은 status 2로 변경되면서 새로운  order number 부여.
        """

        order_info["order_number"] = str(datetime.now()).replace(" ", "")
        
        order_dao = OrderDao()
        order_id  = order_dao.post_order(order_info, connection)
    
        cart_info = {
            "order_id": order_id
        }
        
        updated_cart = []
        for cart_id in order_info["items"]:
            cart_info["cart_id"] = cart_id
            updated_cart.append(order_dao.patch_cart(cart_info, connection))

        return {'data': updated_cart}