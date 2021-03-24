import pymysql

CURRENT_ORDER = '준비중'
CURRENT_CART = 'current'

class OrderDao:
    def __init__(self):
        pass

    def find_current_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            find_order_query = """
                SELECT * FROM orders
                WHERE order_status_type_id = (
                    SELECT id FROM order_status_types WHERE name = '준비중') AND
                    user_id = %(user_id)s
            """
            cursor.execute(find_order_query, order_info)
            order = cursor.fetchone()
        return order

    def find_existing_product_option_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            find_existing_product_option_in_cart = """
                SELECT id, product_option_id, cart_number, calculated_price FROM carts
                WHERE product_option_id = (
                    SELECT id FROM product_options WHERE product_color_type_id = (
                        SELECT id FROM product_color_types WHERE name = %(color)s)
                    AND product_size_type_id = (
                        SELECT id FROM product_size_types WHERE name = %(size)s))
                    AND order_id = %(order_id)s
            """
            cursor.execute(find_existing_product_option_in_cart, order_info)
            existing_product_option_cart = cursor.fetchone()
        return existing_product_option_cart

    def find_product_option(self, order_info, connection):
        with connection.cursor(pymysql.Cursors.DictCursor) as cursor:
            find_product_option_query = """
                SELECT * FROM product_options
                WHERE product_color_type_id = (
                    SELECT id FROM product_color_types WHERE name = %(color)s
                ) AND product_size_type_id = (
                    SELECT id FROM product_size_types WHERE name = %(size)s
                ) AND product_id = %(product_id)s
            """
            cursor.execute(find_product_option_query, order_info)
            product_option_id = cursor.fetchone()
        return product_option_id

    def update_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            update_cart_query = """
                UPDATE carts
                SET quantity = quantity + %(quantity)s
                WHERE id = %(cart_id)s
            """
            cursor.execute(update_cart_query, order_info)
            updated_cart = cursor.lastrowid
        return updated_cart

    def update_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            update_order_query = """
                UPDATE orders
                SET total_price = total_price + %(added_price)s, updated_at = NOW()
                WHERE id = %(order_id)s
            """
            cursor.execute(update_order_query, order_info)
            updated_order = cursor.lastrowid
        return updated_order

    def create_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            create_order_query = """
            INSERT INTO orders(
                order_status_type,
                user_id,
                created_at,
                updated_at,
                order_number,
            ) VALUES(
                3,
                %(user_id)s,
                NOW(),
                NOW(),
                FLOOR(RAND() * 901) + 100
            )
            """
            cursor.execute(create_order_query, order_info)
            new_order = cursor.lastrowid
        return new_order

    def get_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            create_order_query = """
                SELECT * FROM orders
                WHERE id = %(order_id)s
            """
            cursor.execute(create_order_query, order_info)
            new_order = cursor.fetchone()
        return new_order

    def create_order_log(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            create_order_log_query = """
            INSERT INTO order_logs(
                order_id,
                order_status_type_id,
                shipping_info_id,
                user_id,
                created_at,
                updated_at,
                total_price,
                order_number,
                changer_id,
                change_date
            ) VALUES(
                %(order_id)s,
                3,
                1,
                %(user_id)s,
                %(created_at)s,
                %(updated_at)s,
                %(total_price)s,
                %(order_number)s,
                %(user_id)s,
                %(updated_at)s
            )
            """
            cursor.execute(create_order_log_query, order_info)
            new_order_log_id = cursor.lastrowid
        return new_order_log_id

    def create_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            create_cart_query = """
                INSERT INTO carts(
                    product_option_id,
                    order_id,
                    cart_status_type_id,
                    quantity,
                    calculated_price,
                    cart_number,
                    is_paid
                ) VALUES(
                    %(product_option_id)s,
                    %(order_id)s,
                    4,
                    %(quantity)s,
                    %(price)s,
                    FLOOR(RAND() * 401) + 100,
                    0
                )
            """
            cursor.execute(create_cart_query, order_info)
            new_cart = cursor.lastrowid
        return new_cart

    def get_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            get_cart_query = """
                SELECT * FROM carts
                WHERE id = %(cart_id)s
            """
            cursor.execute(get_cart_query, order_info)
            cart = cursor.fetchone()
        return cart

    def create_cart_log(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            create_cart_log_query = """
            INSERT INTO cart_logs(
                cart_id,
                product_option_id,
                order_id,
                cart_status_type_id,
                quantity,
                calculated_price,
                cart_number,
                is_paid,
                changer_id,
                change_date
            ) VALUES (
                %(cart_id)s,
                %(product_option_id)s,
                %(order_id)s,
                4,
                %(quantity)s,
                %(price)s,
                0,
                %(user_id)s,
                NOW()
            )
            """
            cursor.execute(create_cart_log_query, order_info)
            new_cart_log_id = cursor.lastrowid
        return new_cart_log_id
