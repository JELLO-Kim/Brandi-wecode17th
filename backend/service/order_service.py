from model.order_dao import OrderDao
from exceptions import ApiException, NO_CURRENT_ORDER_EXISTS, NO_CART_EXISTS


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
        2. fetch all carts associated with current order
        3. for each product_option, get product_id, size, color
        4. get total_count of product_options in cart
        """
        try:
            order_dao = OrderDao()
            current_order = order_dao.find_current_order(order_info, connection)

            if not current_order:
                raise ApiException(400, NO_CURRENT_ORDER_EXISTS)

            order_info['order_id'] = current_order['id']
            total_cart_number = order_dao.count_carts(order_info, connection)
            cart_details = [{'totalCarts': total_cart_number['count']}]
            all_carts = order_dao.get_all_carts(order_info, connection)

            for cart in all_carts:
                order_info['cart_id'] = cart['id']
                order_info['quantity'] = cart['quantity']
                order_info['product_option_id'] = cart['product_option_id']
                product_option = order_dao.get_product_option(order_info, connection)
                order_info['product_id'] = product_option['product_id']
                order_info['product_size_type_id'] = product_option['product_size_type_id']
                order_info['product_color_type_id'] = product_option['product_color_type_id']
                color_name = order_dao.get_color(order_info, connection)
                size_name = order_dao.get_size(order_info, connection)
                order_info['color'] = color_name['name']
                order_info['size'] = size_name['name']
                cart_details.append(
                    {
                        'productId': order_info['product_id'],
                        'color': order_info['color'],
                        'size': order_info['size'],
                        'quantity': order_info['quantity']
                    }
                )
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
            find_cart = order_dao.find_existing_product_option_cart(order_info, connection)
            if not find_cart:
                raise ApiException(400, NO_CART_EXISTS)
            order_info['cart_id'] = find_cart['id']
            deleted_cart = order_dao.soft_delete_cart(order_info, connection)
            return deleted_cart

        except ApiException as e:
            raise e
