from model.order_dao import OrderDao
from responses import ApiException, NO_CURRENT_ORDER_EXISTS, NO_CART_EXISTS
from flask           import jsonify, json
from datetime        import date, datetime

class OrderService:
    def __init__(self):
        pass

    def post_cart(self, order_info, products, connection):
        """
        logic flow:
        1. 유저가 결제전인 order를 갖고 있는지를 확인한다
            1. 결제전인 order를 갖고 있으면 카트에 이미 담긴 product를 추가하고 있는지를 확인한
            2. 카트에 이미 담긴 product를 추가하고 있으면 카트의 수량을 업데이트 한다
            3. Order의 total_price랑 updated_at을 업데이트 한다
            4. Order 이력을 생성한다
        2. 유저가 새 product를 카트에 담고싶을때 새 카트를 생성한다
            1. Order의 total_price랑 updated_at을 업데이트 한다
            2. Cart이력을 생성한다
            3. Order이력을 생성한다
        3. 유저가 결제전인 order가 없으면
            1. 결제전인 Order를 생성한다
            2. Cart를 생성한다
            3. Order의 total_price를 업데이트한다
            4. Order이력을 생성한다
            5. Cart이력을 생성한다
        """
        order_dao = OrderDao()
        #유저가 결제전인 order (order_status_type)를 갖고 있는지 확인
        current_order = order_dao.find_current_order(order_info, connection)
        #유저가 결제전인 order를 갖고 있으면:
        if current_order:
            order_info['order_id'] = current_order['id']
            order_info['created_at'] = current_order['created_at']

            for product in products:
                # 유저가 카트에 이미 있는 product를 추가할때 카트 수량(quantity)을 업데이트 한다
                order_info['color'] = product['color']
                order_info['size'] = product['size']
                order_info['quantity'] = product['quantity']
                order_info['price'] = product['price']
                existing_product_option_cart = order_dao.find_existing_product_option_cart(order_info, connection)

                if existing_product_option_cart:
                    order_info['cart_id'] = existing_product_option_cart['id']
                    order_info['added_price'] = order_info['quantity'] * existing_product_option_cart['calculated_price']
                    order_dao.update_cart(order_info, connection) #카트 수량을 업데이트한다

                    order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                    order_dao.create_order_log(order_info, connection) #create order_log

                #유저가 새 상품을 카트에 담을때
                else:
                    product_option = order_dao.find_product_option(order_info, connection)
                    order_info['product_option_id'] = product_option['id']

                    new_cart = order_dao.create_cart(order_info, connection) #create new cart
                    order_info['cart_id'] = new_cart
                    order_dao.create_cart_log(order_info, connection) #create cart log
                    get_new_cart = order_dao.get_cart(order_info, connection)
                    order_info['added_price'] = order_info['quantity'] * get_new_cart['calculated_price']

                    order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                    order_dao.create_order_log(order_info, connection) #create order_log
            return True

        #유저가 결제전인 order가 없을때:
        else:
            for product in products:
                order_info['color'] = product['color']
                order_info['size'] = product['size']
                order_info['quantity'] = product['quantity']
                order_info['price'] = product['price']

                new_order = order_dao.create_order(order_info, connection)
                order_info['order_id'] = new_order
                product_option = order_dao.find_product_option(order_info, connection)
                order_info['product_option_id'] = product_option['id']

                new_cart = order_dao.create_cart(order_info, connection)
                order_info['cart_id'] = new_cart
                get_new_cart = order_dao.get_cart(order_info, connection)
                order_dao.create_cart_log(order_info, connection)
                order_info['added_price'] = order_info['quantity'] * get_new_cart['calculated_price']

                order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                order_dao.create_order_log(order_info, connection)
            return True

    def get_cart(self, order_info, connection):
        """
        logic flow:
        1. find if user has existing order
            - if no, raise ERROR
        2. fetch order_id
        2. get total_count of product_options in cart
        3. fetch all DISTINCT seller_ids associated with order_id
        4. for each seller_id (associated with order_id), fetch all associated product_details
        5. for each product_detail, fetch all info about product displayed in cart
        6. return dict of products in cart, grouped by brand_name
        """
        try:
            order_dao = OrderDao()
            current_order = order_dao.find_current_order(order_info, connection)

            if not current_order:
                raise ApiException(400, NO_CURRENT_ORDER_EXISTS)

            order_info['order_id'] = current_order['id']
            total_cart_number = order_dao.count_carts(order_info, connection)
            cart_details = {'totalCount': total_cart_number['count']}
            all_seller_ids = order_dao.get_all_seller_ids(order_info, connection)
            cart_list = []

            for seller_id in all_seller_ids:
                order_info['seller_id'] = seller_id['seller_id']
                brand_name = order_dao.get_brand_name(order_info, connection)
                brand_dict = {'brandName': brand_name['korean_brand_name']}
                product_details = order_dao.get_product_details(order_info, connection)
                brand_dict['detail'] = [
                    {
                        'id': product_detail['id'],
                        'name': product_detail['name'],
                        'price': product_detail['price'],
                        'quantity': product_detail['quantity'],
                        'imageUrl': product_detail['image'],
                        'color': product_detail['color'],
                        'size': product_detail['size']
                    } for product_detail in product_details
                ]
                cart_list.append(brand_dict)
            cart_details['cartList'] = cart_list
            return cart_details
        except ApiException as e:
            raise e

    def delete_cart(self, order_info, connection):
        """
        logic flow:
        1. find if user has existing order
            - if no, raise ERROR
        2. find cart with product_id
            - if no such cart, raise ERROR
        3. change is_delete to 1 in corresponding cart
        """
        try:
            order_dao = OrderDao()
            current_order = order_dao.find_current_order(order_info, connection)
            if not current_order:
                raise ApiException(400, NO_CURRENT_ORDER_EXISTS)

            order_info['order_id'] = current_order['id']
            for product_option_id in order_info['product_option_ids']:
                order_info['product_option_id'] = product_option_id
                find_cart = order_dao.get_cart_delete(order_info, connection)
                if not find_cart:
                    raise ApiException(400, NO_CART_EXISTS)

                order_info['cart_id'] = find_cart['id']
                order_dao.soft_delete_cart(order_info, connection)
                order_dao.create_cart_log(order_info, connection)
            return True
        except ApiException as e:
            raise e



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
