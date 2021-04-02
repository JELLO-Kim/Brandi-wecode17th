import pymysql


class OrderDao:
    def find_current_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """ 
                SELECT
                    id,
                    order_status_type_id,
                    user_id,
                    shipping_info_id,
                    created_at,
                    updated_at,
                    total_price,
                    order_number,
                    is_delete
                FROM
                    orders
                WHERE
                    order_status_type_id = (
                        SELECT id FROM order_status_types WHERE name = '결제전')
                AND
                    user_id = %(user_id)s
            """
            cursor.execute(query, order_info)
            order = cursor.fetchone()
        return order

    def find_existing_product_option_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id, 
                    product_option_id,
                    cart_number,
                    calculated_price
                FROM
                    carts
                WHERE
                    product_option_id = (
                        SELECT id FROM product_options WHERE product_color_type_id = 
                            (SELECT id FROM product_color_types WHERE name = %(color)s)
                        AND product_size_type_id = 
                            (SELECT id FROM product_size_types WHERE name = %(size)s)
                        AND product_id = %(product_id)s
                    )
                AND 
                    order_id = %(order_id)s
            """
            cursor.execute(query, order_info)
            existing_product_option_cart = cursor.fetchone()
        return existing_product_option_cart

    def find_product_option(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT * 
                FROM 
                    product_options
                WHERE 
                    product_color_type_id = 
                        (SELECT id FROM product_color_types WHERE name = %(color)s) 
                    AND 
                        product_size_type_id = 
                            (SELECT id FROM product_size_types WHERE name = %(size)s) 
                    AND 
                        product_id = %(product_id)s
            """
            cursor.execute(query, order_info)
            product_option_id = cursor.fetchone()
        return product_option_id

    def update_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    carts
                SET
                    quantity = quantity + %(quantity)s
                WHERE
                    id = %(cart_id)s
            """
            cursor.execute(query, order_info)
            updated_cart = cursor.lastrowid
        return updated_cart

    def update_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    orders
                SET
                    total_price = total_price + %(added_price)s, updated_at = NOW()
                WHERE
                    id = %(order_id)s
            """
            cursor.execute(query, order_info)
            updated_order = cursor.lastrowid
        return updated_order

    def create_order(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO orders(
                    order_status_type_id,
                    user_id,
                    created_at,
                    updated_at,
                    order_number
                ) VALUES(
                    1,
                    %(user_id)s,
                    NOW(),
                    NOW(),
                    FLOOR(RAND() * 901) + 100
                )
            """
            cursor.execute(query, order_info)
            new_order = cursor.lastrowid
        return new_order

    def create_order_log(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO order_logs(
                    order_id,
                    order_status_type_id,
                    user_id,
                    created_at,
                    updated_at,
                    total_price,
                    order_number,
                    changer_id,
                    change_date
                ) VALUES(
                    %(order_id)s,
                    1,
                    %(user_id)s,
                    (SELECT created_at from orders WHERE id = %(order_id)s),
                    (SELECT updated_at from orders WHERE id = %(order_id)s),
                    (SELECT total_price from orders WHERE id = %(order_id)s),
                    (SELECT order_number from orders WHERE id = %(order_id)s),
                    %(user_id)s,
                    (SELECT updated_at from orders WHERE id = %(order_id)s)
                )
            """
            #include shipping_info_id (make sure to account for order_view if user has shipping_info_id)
            cursor.execute(query, order_info)
            new_order_log_id = cursor.lastrowid
        return new_order_log_id

    def create_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
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
                    1,
                    %(quantity)s,
                    %(price)s,
                    FLOOR(RAND() * 401) + 100,
                    0
                )
            """
            cursor.execute(query, order_info)
            new_cart = cursor.lastrowid
        return new_cart

    def get_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT * FROM carts
                WHERE id = %(cart_id)s
            """
            cursor.execute(query, order_info)
            cart = cursor.fetchone()
        return cart

    def create_cart_log(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO cart_logs(
                    cart_id,
                    product_option_id,
                    order_id,
                    cart_status_type_id,
                    quantity,
                    calculated_price,
                    cart_number,
                    is_paid,
                    is_delete,
                    changer_id,
                    change_date
                ) VALUES (
                    %(cart_id)s,
                    (SELECT product_option_id FROM carts WHERE id = %(cart_id)s),
                    %(order_id)s,
                    (SELECT cart_status_type_id FROM carts WHERE id = %(cart_id)s),
                    (SELECT quantity FROM carts WHERE id = %(cart_id)s),
                    (SELECT calculated_price FROM carts WHERE id = %(cart_id)s),
                    (SELECT cart_number FROM carts WHERE id = %(cart_id)s),
                    (SELECT is_paid FROM carts WHERE id = %(cart_id)s),
                    (SELECT is_delete FROM carts WHERE id = %(cart_id)s),
                    %(user_id)s,
                    NOW()
                )
            """
            cursor.execute(query, order_info)
            new_cart_log_id = cursor.lastrowid
        return new_cart_log_id

    def get_brand_name(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    korean_brand_name
                FROM
                    sellers
                WHERE
                    user_info_id = %(seller_id)s 
            """
            cursor.execute(query, order_info)
            brand_name = cursor.fetchone()
        return brand_name

    def get_all_seller_ids(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    DISTINCT p.seller_id
                FROM
                    products AS p
                INNER JOIN product_options AS po
                    ON p.id = po.product_id
                INNER JOIN carts AS c
                    ON po.id = c.product_option_id
                INNER JOIN orders AS o
                    ON c.order_id = o.id
                INNER JOIN order_status_types AS os
                    ON o.order_status_type_id = os.id
                WHERE
                    o.id = %(order_id)s
                AND
                    order_status_type_id = 1
                AND
                    c.is_delete = 0
            """
            cursor.execute(query, order_info)
            seller_ids = cursor.fetchall()
        return seller_ids

    def get_product_details(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    po.id,
                    p.name,
                    p.price,
                    c.quantity,
                    pt.image_url AS image,
                    pc.name as color,
                    ps.name as size
                FROM 
                    product_options AS po
                INNER JOIN product_color_types AS pc
                    ON po.product_color_type_id = pc.id
                INNER JOIN product_size_types AS ps
                    ON po.product_size_type_id = ps.id
                INNER JOIN products AS p
                    ON po.product_id = p.id
                INNER JOIN product_thumbnails AS pt
                    ON p.id = pt.product_id
                INNER JOIN carts AS c
                    ON po.id = c.product_option_id
                INNER JOIN orders AS o
                    ON c.order_id = o.id
                WHERE 
                    p.seller_id = %(seller_id)s 
                AND 
                    order_id = %(order_id)s 
                AND 
                    pt.ordering = 1
                AND
                    c.is_delete = 0
            """
            cursor.execute(query, order_info)
            product_details = cursor.fetchall()
        return product_details

    def count_carts(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    COUNT(*) AS count
                FROM
                    carts
                WHERE
                    order_id = %(order_id)s
                AND
                    carts.is_delete = 0
            """
            cursor.execute(query, order_info)
            total_carts = cursor.fetchone()
        return total_carts

    def get_cart_delete(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    c.id
                FROM
                    carts AS c
                INNER JOIN product_options AS po
                    ON c.product_option_id = po.id
                INNER JOIN orders AS o
                    ON c.order_id = o.id
                WHERE
                    order_id = %(order_id)s
                AND 
                    po.id = %(product_option_id)s
            """
            cursor.execute(query, order_info)
            cart_to_delete = cursor.fetchone()
        return cart_to_delete

    def soft_delete_cart(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE
                carts
            SET
                is_delete = 1
            WHERE
                id = %(cart_id)s
            """
            cursor.execute(query, order_info)
            deleted_cart = cursor.lastrowid
        return deleted_cart


    def get_address(self, user_id, connection):

        """
        해당 회원 계정으로 주문한 지난배송지 목록.
        기본배송지로 지정된 배송지(default=1)가 최상위, 그 뒤로 ordering 순서로 나열.
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
             SELECT
                s.id,
                s.recipient_name AS name,
                s.recipient_phone AS phone,
                s.recipient_postal_code AS postal,
                s.recipient_address AS address,
                s.recipient_address_detail AS addressDetail,
                s.is_default as isDefault
            FROM
                shipping_info AS s
            WHERE s.user_id = %(user_id)s
            ORDER BY isDefault DESC, ordering ASC
            """
            cursor.execute(query, {"user_id" : user_id})

            return {"data": cursor.fetchall()}


    def post_address(self, address_info, connection):
        
        """
        주문시 기존 주문내역에 있는 배송지가 아닌 새 배송지를 입력하는경우 db에 추가
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO shipping_info (
                user_id,
                recipient_name,
                recipient_phone,
                recipient_postal_code,
                recipient_address,
                recipient_address_detail,
                is_default
            ) VALUES (
                %(user_id)s,
                %(recipient_name)s,
                %(recipient_phone)s,
                %(recipient_postal_code)s,
                %(recipient_address)s,
                %(recipient_address_detail)s,
                %(is_detail)s
            )
            """
            cursor.execute(query, address_info)

            return cursor.lastrowid


    def post_order(self, order_info, connection):
        
        """
        order 테이블에 status=1로 장바구니에 담겨있는 상품들이 결제되므로 patch 함수로 결제되는 상품들만 status=2 로 변경.
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            order = """
            INSERT INTO orders(
                order_status_type_id,
                user_id,
                order_name,
                order_phone,
                order_email,
                shipping_info_id,
                shipping_memo_type_id,
                created_at,
                updated_at,
                total_price,
                order_number,
                is_delete
            ) VALUES (
                2,
                %(user_id)s,
                %(order_name)s,
                %(order_phone)s,
                %(order_email)s,
                %(shipping_info_id)s,
                %(shipping_memo_id)s,
                NOW(),
                NOW(),
                %(total_price)s,
                %(order_number)s,
                0
            )
            """
            # updated_at을 우선에 결제시간으로 - 수정필요
            ## transaction 걸기
            cursor.execute(order, order_info)
            return cursor.lastrowid


    def patch_cart(self, cart_info, connection):
        
        """
        order 테이블에 status=1로 장바구니에 담겨있는 상품들이 결제되므로 patch 함수로 결제되는 상품들만 status=2 로 변경.
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cart = """
            UPDATE carts
            SET 
                order_id = %(order_id)s,
                cart_status_type_id = 1
            WHERE id = %(cart_id)s
            """
            #1 = 확정대기
            cursor.execute(cart, cart_info)
            return cursor.lastrowid
