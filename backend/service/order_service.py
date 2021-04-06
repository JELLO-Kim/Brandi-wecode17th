from model.order_dao import OrderDao
from responses import *
from flask           import jsonify, json
from datetime        import date, datetime
from utils import login_decorator

CURRENT_ORDER_STATUS_TYPE = 1


class OrderService:
    def __init__(self):
        pass

    def post_cart(self, order_info, products, connection):
        """
        Author: Mark Hasung Kim
        Args:
            order_info (dict): 유저 주문 관련 정보
            products (dict): 카트에 담길 products에대한 정보 (color, size, quantity, price)
            connection: 커넥션
        Returns: True (카트에 상품이 성공적으로 담기면 True를 반환해준다)
        """
        order_dao = OrderDao()
        #유저가 결제전인 order (order_status_type)를 갖고 있는지 확인
        order_info['order_status_type_id'] = CURRENT_ORDER_STATUS_TYPE
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
                    order_dao.create_cart_log(order_info, connection)
                    order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                    order_dao.create_order_log(order_info, connection) #create order_log

                #유저가 새 상품을 카트에 담을때
                else:
                    product_option = order_dao.find_product_option(order_info, connection)

                    if not product_option:
                        raise ApiException(400, INVALID_PRODUCT_OPTION)

                    order_info['product_option_id'] = product_option['id']

                    new_cart = order_dao.create_cart(order_info, connection) #create new cart
                    order_info['cart_id'] = new_cart
                    order_dao.create_cart_log(order_info, connection) #create cart log
                    get_new_cart = order_dao.get_cart(order_info, connection)
                    order_info['added_price'] = order_info['quantity'] * get_new_cart['calculated_price']

                    order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                    order_dao.create_order_log(order_info, connection) #create order_log
            return True

        #유저가 결제전인 order이 없을때:
        else:
            for product in products:
                order_info['color'] = product['color']
                order_info['size'] = product['size']
                order_info['quantity'] = product['quantity']
                order_info['price'] = product['price']

                new_order = order_dao.create_order(order_info, connection)
                order_info['order_id'] = new_order
                product_option = order_dao.find_product_option(order_info, connection)

                if not product_option:
                    raise ApiException(400, INVALID_PRODUCT_OPTION)

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
        Author: Mark Hasung Kim
        Args:
            order_info (dict): 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            cart_details (유저 카트에 담긴 모든 상품 정보)
        """
        try:
            order_dao = OrderDao()
            order_info['order_status_type_id'] = CURRENT_ORDER_STATUS_TYPE
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
                        'product_option_id': product_detail['product_option_id'],
                        'cart_id': product_detail['cart_id'],
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
        Author: Mark Hasung Kim
        Args:
            order_info (dict): 유저 주문 관련 정보
            connection: 커넥션
        Returns: True (카트가 삭제돼면 True를 반환해준다)

        """
        try:
            order_dao = OrderDao()
            order_info['order_status_type_id'] = CURRENT_ORDER_STATUS_TYPE
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

    def get_shipping_memo(self, connection):

        """
        배송메모 목록
        """

        order_dao   = OrderDao()
        shipping_memo = order_dao.get_shipping_memo(connection)

        return {'data': shipping_memo}


    def get_address(self, user_id, connection):

        """
        이전 배송지 목록 가져오기
        """

        order_dao   = OrderDao()
        get_address = order_dao.get_address(user_id, connection)

        return {'data': get_address}

    
    def delete_address(self, address_info, connection):

        order_dao   = OrderDao()
        address_id = order_dao.delete_address(address_info, connection)

        return {'data': address_id}


    def direct_purchase(self, order_info, products, connection):
        order_dao = OrderDao()
        order_id = order_dao.create_order(order_info, connection)
        order_info["order_id"] = order_id 
        order_log = order_dao.post_order_log(order_info, connection)
        # connection.commit()

        order_info["order_status_type_id"] = 3
        cart= []

        for product in products:

            if "color" not in product:
                raise ApiException(400, COLOR_NOT_IN_INPUT)

            order_info["color"]    = product["color"]

            if "size" not in product:
                raise ApiException(400, SIZE_NOT_IN_INPUT)

            order_info["size"]                = product["size"]
            order_info["quantity"]            = product["quantity"]
            order_info["price"]               = product["price"] 
            product_option_id                 = order_dao.find_product_option_id(order_info, connection)
            order_info["product_option_id"]   = product_option_id["id"]
            order_info["cart_status_type_id"] = 3
            cart_id                           = order_dao.create_cart(order_info, connection)
            cart.append(cart_id)


        return {'orderId': order_id, 'items': cart}


    def post_address(self, address_info, connection):
        
        """
        배송지 신규 등록
        """
        
        order_dao    = OrderDao()
        user_id = address_info["user_id"]
        address_all = order_dao.get_address(user_id, connection)

        for address in address_all:
            if address["address"] == address_info["recipient_address"] and address["addressDetail"] == address_info["recipient_address_detail"]:
                raise ApiException(400, "이미 존재하는 주소입니다")
        
        if address_info["is_default"] in ["1", 1]:
            reset                    = order_dao.reset_address_default(address_info, connection)
            address_info["shipping_info_id"] = reset
            reset_log                = order_dao.post_address_log(address_info, connection)
        
        address_id                 = order_dao.post_address(address_info, connection)
        address_info["shipping_info_id"] = address_id
        address_log                = order_dao.post_address_log(address_info, connection)

        return {'data': address_id}


    def order_confirm(self, order_info, connection):
        
        """
        order table에서 status=1로 장바구니 상태인 상품들 중 결제 된 상품들은 status 2로 변경되면서 새로운  order number 부여.
        """

        order_dao  = OrderDao()
        order_id = order_dao.create_order_fullinfo(order_info, connection)

        order_info["order_id"] = order_id
        order_log  = order_dao.post_order_log(order_info, connection)
    
        for item in order_info["items"]:
            order_info["cart_id"] = item
            cart_id  = order_dao.patch_cart(order_info, connection)
            cart_log = order_dao.create_cart_log(order_info, connection)

        return {"data" : order_info["order_id"]}
