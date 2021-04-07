from model.order_dao import OrderDao
from responses import *

CURRENT_ORDER_STATUS_TYPE = 1


class OrderService:
    def __init__(self):
        pass

    def post_cart(self, order_info, products, connection):
        """ [서비스] 카트 생성하기
        Author: Mark Hasung Kim
        Args:
            order_info (dict): 유저 주문 관련 정보
            products (dict): 카트에 담길 products에대한 정보 (color, size, quantity, price)
            connection: 커넥션
        Returns:
            True (카트에 상품이 성공적으로 담기면 True를 반환해준다)
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
        """ [서비스] 유저의 모든 카트를 갖고오기
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
        """ [서비스] 카트 soft delete
        Author: Mark Hasung Kim
        Args:
            order_info (dict): 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            True (카트가 삭제돼면 True를 반환해준다)
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
        """ [서비스] 결제페이지 (배송정보 입력 후 결제 버튼 누른 다음)
        Author:
            Ji Yoon Lee
        Returns:
            {'data': shipping_memo} ; 배송메모 리스트를 'data'라는 키값에 넣어서 반환
        """
        order_dao = OrderDao()
        shipping_memo = order_dao.get_shipping_memo(connection)

        return {'data': shipping_memo}


    def get_address(self, user_id, connection):
        """ [서비스] 배송지 목록 가져오기
        Author:
            Ji Yoon Lee
        Args:
            user_id(str): 로그인한 user id
        Returns:
            {'data': get_address} ; 해당 사용자의 과거 배송지를 'data'라는 키값에 넣어서 반환
        """
        order_dao = OrderDao()
        get_address = order_dao.get_address(user_id, connection)

        return {'data': get_address}

    
    def delete_address(self, address_info, connection):
        """ [서비스] 기존 배송지 삭제
        Author:
            Ji Yoon Lee
        Args:
            address_info(dict): 배송지 정보
        Returns:
            {'data': address_id} ; 삭제된 배송지의 id를 'data'라는 키값에 넣어서 반환
        """
        order_dao = OrderDao()
        address_id = order_dao.delete_address(address_info, connection)

        return {'data': address_id}

    def direct_purchase(self, order_info, products, connection):
        """ [서비스] 바로결제
        Author:
            Ji Yoon Lee
        Args:
            order_info(dict)
            products(dict)
        Returns:
            {'data': get_address}; 해당 사용자의 과거 배송지를 'data'라는 키값에 넣어서 반환
        """
        order_dao = OrderDao()
        order_id = order_dao.create_order(order_info, connection)
        order_info['order_id'] = order_id 
        order_log = order_dao.post_order_log(order_info, connection)
        order_info['order_status_type_id'] = 3
        cart = []

        for product in products:
            order_info['color'] = product['color']
            order_info['size'] = product['size']
            order_info['quantity'] = product['quantity']
            order_info['price'] = product['price'] 
            product_option_id = order_dao.find_product_option_id(order_info, connection)
            
            if product_option_id is None:
                raise ApiException(400, PRODUCT_OPTION_NOT_EXISTING)

            order_info['product_option_id'] = product_option_id['id']
            order_info['cart_status_type_id'] = 3
            # 바로결제 시도시 cart_status_type_id = 3
            cart_id = order_dao.create_cart(order_info, connection)
            cart.append(cart_id)

        return {'orderId': order_id, 'items': cart}


    def post_address(self, address_info, connection):
        """ [서비스] 신규 배송지 추가
        Author:
            Ji Yoon Lee
        Args:
            address_info(dict)
        Returns:
            {'data': address_id}; 추가된 배송지의 id값을 'data'라는 키값에 넣어서 반환
        """
        order_dao = OrderDao()
        user_id = address_info['user_id']
        address_all = order_dao.get_address(user_id, connection)
        default_address = None

        # 해당 유저가 이미 등록한 배송지인지 검사
        for address in address_all:
            if address['address'] == address_info['recipient_address'] and address['addressDetail'] == address_info['recipient_address_detail']:
                raise ApiException(400, ADDRESS_ALREADY_EXISTS)

            if address_info['is_default'] in ['1', 1]:
                default_address = address['id']
        
        # 기본배송지가 이미 존재하는데, 새로추가된 배송지를 기본배송지로 등록할 때 - 기존 배송지 기본배송지 해제
        if address_info['is_default'] in ['1', 1]:
            if order_dao.reset_address_default(address_info, connection) == False:
                raise ApiException(400, REQUEST_FAILED)
            address_info['shipping_info_id'] = default_address
            reset_log = order_dao.post_address_log(address_info, connection)
        
        # 신규 배송지 등록
        address_id = order_dao.post_address(address_info, connection)
        address_info['shipping_info_id'] = address_id
        address_log = order_dao.post_address_log(address_info, connection)

        return {'data': address_id}


    def order_confirm(self, order_info, connection):
        """ [서비스] 배송지입력 후 결제버튼 눌렀을 때 오는 요청
        Author:
            Ji Yoon Lee
        Args:
            order_info(dict)
        Returns:
            {'data': get_address} : 해당 사용자의 과거 배송지를 'data'라는 키값에 넣어서 반환
        """
        # 새로운 결제완료 order 생성
        order_dao = OrderDao()
        order_id = order_dao.create_order_fullinfo(order_info, connection)
        order_info['order_id'] = order_id
        order_log = order_dao.post_order_log(order_info, connection)
    
        # 새로 생성된 order를 Foreign Key로 가지고있는 카트(각각의 아이템)의 상태도 결제완료로 업데이트
        for item in order_info['items']:
            order_info['cart_id'] = item
            cart_id = order_dao.patch_cart(order_info, connection)
            cart_log = order_dao.create_cart_log(order_info, connection)

        return {'data': order_info['order_id']}
