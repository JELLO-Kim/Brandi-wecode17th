from flask import jsonify
from model.order_dao import OrderDao


class OrderService:
    def __init__(self):
        pass

    def post_cart(self, order_info, connection):
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

            for product in order_info['products']:
                # 유저가 카트에 이미 있는 product를 추가할때 카트 수량(quantity)을 업데이트 한다
                order_info['color'] = product['color']
                order_info['size'] = product['size']
                order_info['quantity'] = product['quantity']
                existing_product_option_cart = order_dao.find_existing_product_option_cart(order_info, connection)

                if existing_product_option_cart:
                    order_info['cart_id'] = existing_product_option_cart['id']
                    order_info['added_price'] = order_info['quantity'] * existing_product_option_cart['calculated_price']
                    updated_cart = order_dao.update_cart(order_info, connection) #카트 수량을 업데이트한다

                    order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                    updated_order = order_dao.get_order(order_info, connection)
                    order_info['total_price'] = updated_order['total_price']
                    order_info['updated_at'] = updated_order['updated_at']
                    order_info['order_number'] = updated_order['order_number']
                    order_dao.create_order_log(order_info, connection) #create order_log
                    return updated_cart

                #유저가 새 상품을 카트에 담을때
                product_option = order_dao.find_product_option(order_info, connection)
                order_info['product_option_id'] = product_option['id']

                new_cart = order_dao.create_cart(order_info, connection) #create new cart
                order_info['cart_id'] = new_cart
                order_dao.create_cart_log(order_info, connection) #create cart log
                get_new_cart = order_dao.get_cart(order_info, connection)
                order_info['added_price'] = order_info['quantity'] * get_new_cart['calculated_price']

                updated_order = order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
                order_info['order_id'] = updated_order
                get_updated_order = order_dao.get_order(order_info, connection)
                order_info['total_price'] = get_updated_order['total_price']
                order_info['updated_at'] = get_updated_order['updated_at']
                order_info['order_number'] = get_updated_order['order_number']
                order_dao.create_order_log(order_info, connection) #create order_log
                return new_cart

        #유저가 결제전인 order가 없을때:
        for product in order_info['products']:
            order_info['color'] = product['color']
            order_info['size'] = product['size']
            order_info['quantity'] = product['quantity']

            new_order = order_dao.create_order(order_info, connection)
            order_info['order_id'] = new_order
            get_new_order = order_dao.get_order(order_info, connection)
            order_info['created_at'] = get_new_order['created_at']
            product_option = order_dao.find_product_option(order_info, connection)
            order_info['product_option_id'] = product_option['id']

            new_cart = order_dao.create_cart(order_info, connection)
            order_info['cart_id'] = new_cart
            get_new_cart = order_dao.get_cart(order_info, connection)
            order_dao.create_cart_log(order_info, connection)
            order_info['added_price'] = order_info['quantity'] * get_new_cart['calculated_price']

            updated_order = order_dao.update_order(order_info, connection) #Order total_price랑 updated_at을 업데이트한다
            order_info['order_id'] = updated_order
            get_updated_order = order_dao.get_order(order_info, connection)
            order_info['total_price'] = get_updated_order['total_price']
            order_info['updated_at'] = get_updated_order['updated_at']
            order_info['order_number'] = get_updated_order['order_number']
            order_dao.create_order_log(order_info, connection)

            return new_cart
