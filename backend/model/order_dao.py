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
                    order_number,
                    payment
                ) VALUES(
                    %(order_status_type_id)s,
                    %(user_id)s,
                    NOW(),
                    NOW(),
                    FLOOR(RAND() * 901) + 100,
                    NOW()
                )
            """
            # 1=결제전 2=결제후 3 = 바로결제시도
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
            ##post_order_log로 합치기?
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
                    %(cart_status_type_id)s,
                    %(quantity)s,
                    %(price)s,
                    FLOOR(RAND() * 401) + 100,
                    0
                )
            """
            ## cart_status_type_id 값 받아서 넣기 ( 하드코딩 x)
            # 1 = 장바구니, 2 = 결제완료, 3 = 바로결제 시도
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
                ) SELECT
                    %(cart_id)s,
                    product_option_id,
                    order_id,
                    cart_status_type_id,
                    quantity,
                    calculated_price,
                    cart_number,
                    is_paid,
                    is_delete,
                    %(user_id)s,
                    NOW()
                FROM
                    carts
                WHERE carts.id = %(cart_id)s
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



    def get_shipping_memo(self, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                id,
                contents
            FROM
                shipping_memo_types
            """
            cursor.execute(query)

            return cursor.fetchall()


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
            WHERE 
                s.user_id = %(user_id)s
                AND
                s.is_delete = 0
            ORDER BY isDefault DESC, id DESC
            """
            cursor.execute(query, {"user_id" : user_id})

            return cursor.fetchall()


    def delete_address(self, address_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE
                shipping_info
            SET
                is_delete = 1
            WHERE
                id = %(address_id)s
            """
            cursor.execute(query, address_id)
            delete_address = cursor.lastrowid
        return delete_address


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
                is_default,
                created_at,
                updated_at,
                is_delete
            ) VALUES (
                %(user_id)s,
                %(recipient_name)s,
                %(recipient_phone)s,
                %(recipient_postal_code)s,
                %(recipient_address)s,
                %(recipient_address_detail)s,
                %(is_default)s,
                NOW(),
                NOW(),
                0
            )
            """
            cursor.execute(query, address_info)

            return cursor.lastrowid

    def check_duplicated_address(self, address_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                recipient_address AS address,
                recipient_address_detail AS detail
            FROM
                shipping_info
            WHERE
                user_id = %(user_id)s
            """
            cursor.execute(query, address_info)
            return cursor.fetchall()


    def post_address_log(self, address_info, connection):
        
        """
        주문시 기존 주문내역에 있는 배송지가 아닌 새 배송지를 입력하는경우 db에 추가
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO shipping_info_logs (
                shipping_info_id,
                user_id,
                recipient_name,
                recipient_phone,
                recipient_postal_code,
                recipient_address,
                recipient_address_detail,
                is_default,
                is_delete,
                changer_id,
                change_date
            ) SELECT
                %(shipping_info_id)s,
                s.user_id,
                s.recipient_name,
                s.recipient_phone,
                s.recipient_postal_code,
                s.recipient_address,
                s.recipient_address_detail,
                s.is_default,
                s.is_delete,
                %(user_id)s,
                NOW()
            FROM 
                shipping_info AS s
            WHERE s.id = %(shipping_info_id)s
            """
            cursor.execute(query, address_info)

            return cursor.lastrowid

    def reset_address_default(self, address_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            reset = """
            UPDATE 
                shipping_info
            SET 
                is_default = 0
            WHERE 
                user_id = %(user_id)s
            """
            # AND 조건 필요한지 굳이..? (하나의 row를 찾는거 vs 전)
            cursor.execute(reset, address_info)
            
            return cursor.lastrowid
            ## check if this returns the right id number


    def update_order(self, order_info, connection):
        
        """
        order 테이블에 status=1로 장바구니에 담겨있는 상품들이 결제되므로 patch 함수로 결제되는 상품들만 status=2 로 변경.
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE 
                orders
            SET 
                order_status_type_id = 2,
                order_name = %(order_name)s,
                order_phone = %(order_phone)s,
                order_email = %(order_email)s,
                shipping_info_id = %(shipping_info_id)s,
                shipping_memo_type_id = %(shipping_memo_type_id)s,
                updated_at = NOW()
            WHERE 
                id = %(order_id)s
            """
            cursor.execute(query, order_info)
            return cursor.lastrowid


    def find_product_option_id(self, order_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id
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
            return cursor.fetchone()


    def create_order_fullinfo(self, order_info, connection):
        """
        바로결제시
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO orders ( 
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
                is_delete,
                payment
            ) VALUES (
                2,
                %(user_id)s,
                %(order_name)s,
                %(order_phone)s,
                %(order_email)s,
                %(shipping_info_id)s,
                %(shipping_memo_type_id)s,
                NOW(),
                NOW(),
                %(total_price)s,
                FLOOR(RAND() * 401) + 100,
                0,
                NOW()
            )
            """
            cursor.execute(query, order_info)
            return cursor.lastrowid


    def post_order_log(self, order_info, connection):

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO order_logs(
                order_id,
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
                is_delete,
                changer_id,
                change_date
            ) SELECT
                %(order_id)s,
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
                is_delete,
                %(user_id)s,
                NOW()
            FROM
                orders AS o
            WHERE 
                o.id = %(order_id)s
            """
            cursor.execute(query, order_info)
            return cursor.lastrowid

    def patch_cart(self, order_info, connection):
        
        """
        order 테이블에 status=1로 장바구니에 담겨있는 상품들이 결제되므로 patch 함수로 결제되는 상품들만 status=2 로 변경.
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE carts
            SET 
                cart_status_type_id = 2,
                order_id = %(order_id)s
            WHERE id = %(cart_id)s
            """
            #1 = 장바구니, 2 = 결제, 3 = 바로결제 시도 4 = 배송중, 5 = 확정대기, 6 = 취소, 7 = 환불
            cursor.execute(query, order_info)
            return cursor.lastrowid
