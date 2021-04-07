import pymysql


class OrderDao:
    def find_current_order(self, order_info, connection):
        """ [서비스] 유저가 결제전인 order이 있는지 검색
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            order (유저가 결제전인 order이 있으면 그 order겍체를 반환해준다)
        """
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
                    order_status_type_id = %(order_status_type_id)s
                AND
                    user_id = %(user_id)s
            """
            cursor.execute(query, order_info)
            order = cursor.fetchone()
        return order

    def find_existing_product_option_cart(self, order_info, connection):
        """ [서비스] 유저가 카트에 이미 담겨있는 상품을 또 추가할떄
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            existing_product_option_cart (카트 객체)
        """
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
        """ [서비스] 유저가 담고싶은 product_option 찾기
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            product_option_id (product_option 객체)
        """
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
            product_option = cursor.fetchone()
        return product_option

    def update_cart(self, order_info, connection):
        """ [서비스] 카트 업데이트
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            updated_cart_id (업데이트 된 카트 id)
        """
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
        """ [서비스] order 업데이트
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            updated_order (업데이트 왼 order id)
        """
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
        """ [서비스] 결제전인 order 생성
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            new_order (새로 생성된 order 객체)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO orders(
                    order_status_type_id,
                    user_id,
                    created_at,
                    updated_at,
                    order_number
                )
                SELECT
                    %(order_status_type_id)s,
                    %(user_id)s,
                    NOW(),
                    NOW(),
                    MAX(order_number) + 1
                FROM
                    orders
            """
            # 1=결제전 2=결제후 3 = 바로결제시도
            cursor.execute(query, order_info)
            new_order = cursor.lastrowid
        return new_order

    def create_order_log(self, order_info, connection):
        """ [서비스] order_log 생성
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            new_order_log_id (새러 생성된 order_log id)
        """
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
                ) 
                SELECT
                    o.id,
                    o.order_status_type_id,
                    o.user_id,
                    o.created_at,
                    o.updated_at,
                    o.total_price,
                    o.order_number,
                    o.user_id,
                    o.updated_at
                FROM
                    orders AS o
                WHERE
                    o.id = %(order_id)s 
            """
            ##post_order_log로 합치기?
            #include shipping_info_id (make sure to account for order_view if user has shipping_info_id)
            cursor.execute(query, order_info)
            new_order_log_id = cursor.lastrowid
        return new_order_log_id

    def create_cart(self, order_info, connection):
        """ [서비스] 카트 생성
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            new_cart (새로 생성된 카트 id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO carts(
                    product_option_id,
                    order_id,
                    cart_status_type_id,
                    quantity,
                    calculated_price,
                    cart_number
                )
                SELECT
                    %(product_option_id)s,
                    %(order_id)s,
                    %(cart_status_type_id)s,
                    %(quantity)s,
                    %(price)s,
                    MAX(cart_number) + 1
                FROM
                    carts
            """
            ## cart_status_type_id 값 받아서 넣기 ( 하드코딩 x)
            # 1 = 장바구니, 2 = 결제완료, 3 = 바로결제 시도
            cursor.execute(query, order_info)
            new_cart = cursor.lastrowid
        return new_cart

    def get_cart(self, order_info, connection):
        """ [서비스] 새로 생성된 카트의 계산된 가격 (calculated_price) 갖고오기
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            cart (calculated_price들 담긴 카트 객체)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    calculated_price 
                FROM
                    carts
                WHERE
                    id = %(cart_id)s
            """
            cursor.execute(query, order_info)
            cart = cursor.fetchone()
        return cart

    def create_cart_log(self, order_info, connection):
        """ [서비스] cart_log 생성
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            new_cart_log_id (새로 생성된 카트 id)
        """
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
                ) 
                SELECT
                    c.id,
                    c.product_option_id,
                    c.order_id,
                    c.cart_status_type_id,
                    c.quantity,
                    c.calculated_price,
                    c.cart_number,
                    c.is_paid,
                    c.is_delete,
                    %(user_id)s,
                    NOW()
                FROM
                    carts AS c
                WHERE
                    c.id = %(cart_id)s
            """
            cursor.execute(query, order_info)
            new_cart_log_id = cursor.lastrowid
        return new_cart_log_id

    def get_brand_name(self, order_info, connection):
        """ [서비스] 결제전인 order의 모든 상품 브랜드 이름 갖고오기
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            brand_name (한국 브랜드 이름)
        """
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
        """  [서비스] 결제전인 order의 모든 셀러 id 갖고오기
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            seller_ids (distinct한 셀러 id)
        """
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
                    order_status_type_id = %(order_status_type_id)s
                    AND
                    c.is_delete = 0
            """
            cursor.execute(query, order_info)
            seller_ids = cursor.fetchall()
        return seller_ids

    def get_product_details(self, order_info, connection):
        """ [서비스] 유저 카트에 있는 모든 product_option 디테일 정보
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            product_details (모든 product_option 디테일 정보)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    po.id AS product_option_id,
                    c.id AS cart_id,
                    p.name,
                    p.price,
                    c.quantity,
                    pt.image_url AS image,
                    pc.name AS color,
                    ps.name AS size
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
        """ [서비스] 결제전인 카트 개수
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            total_carts (결제전인 카트 개수)
        """
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
        """ [서비스] 유저가 삭제하고싶은 카트 갖고오기
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            cart_to_delete (삭제할 카트 객체)
        """
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
                    AND
                    c.is_delete = 0
            """
            cursor.execute(query, order_info)
            cart_to_delete = cursor.fetchone()
        return cart_to_delete

    def soft_delete_cart(self, order_info, connection):
        """ [서비스] 카트 soft delete 하기 (is_delete = 1)
        Author: Mark Hasung Kim
        Args:
            order_info: 유저 주문 관련 정보
            connection: 커넥션
        Returns:
            deleted_cart (삭제된 카트 id)
        """
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
        """ [서비스] 배송메모 가져오기
        Author:
            Ji Yoon Lee
        Returns:
            배송메모 목록
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                s.id,
                s.contents
            FROM
                shipping_memo_types AS s
            """
            cursor.execute(query)

        return cursor.fetchall()

    def get_address(self, user_id, connection):
        """ [서비스] 배송지 목록 가져오기
        Author:
            Ji Yoon Lee
        Args:
            user_id(str)
        Returns:
            해당 사용자의 배송지 목록
        Note:
            기본배송지로 지정된 배송지(default=1)가 최상위, 그 뒤로 배송지 등록 최신순으로 나열
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
                AND
                s.is_delete = 0
            ORDER BY is_default DESC, id DESC
            """
            cursor.execute(query, {"user_id": user_id})

        return cursor.fetchall()

    def delete_address(self, address_id, connection):
        """ [서비스] 기존 배송지 삭제
        Author:
            Ji Yoon Lee
        Args:
            address_id(str)
        Returns:
            True
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE
                shipping_info AS s
            SET
                s.is_delete = 1
            WHERE 
                s.id = %(address_id)s
                AND 
                s.user_id = %(user_id)s
            """
            cursor.execute(query, address_id)

        return True

    def post_address(self, address_info, connection):
        """ [서비스] 배송지 추가 (배송지 중복 테스트 통과 된 새 배송지)
        Author:
            Ji Yoon Lee
        Args:
            address_info(dict)
        Returns:
            추가된 배송지 address_id
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

    def post_address_log(self, address_info, connection):
        """ [서비스] orders 테이블 변경 이력
        Author:
            Ji Yoon Lee
        Args:
            address_info(dict)
        Returns:
            추가된 orders_log 테이블 id
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
        """ [서비스] 사용자가 이미 기본배송지를 설정해 놓은 경우, 기본배송지 모두 취소
        Author:
            Ji Yoon Lee
        Args:
            address_info(dict)
        Returns:
            True
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            reset = """
            UPDATE 
                shipping_info
            SET 
                is_default = 0
            WHERE 
                user_id = %(user_id)s
                AND
                is_default = 1
            """
            cursor.execute(reset, address_info)
            
            return True

    def find_product_option_id(self, order_info, connection):
        """ [서비스] 상품 옵션 아이디 찾기
        Author:
            Ji Yoon Lee
        Args:
            order_info(dict)
        Returns:
            product_option_id
        Note:
            상품의 색상, 사이즈가 이름으로 들어오면 해당 조합의 option id를 찾는 로직
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    p.id
                FROM
                    product_options AS p
                LEFT JOIN
                    product_color_types AS c
                    ON p.product_color_type_id = c.id
                LEFT JOIN
                    product_size_types AS s
                    ON p.product_size_type_id = s.id
                WHERE
                    c.name = %(color)s
                    AND
                    s.name = %(size)s
                    AND
                    p.product_id = %(product_id)s
                """
            cursor.execute(query, order_info)
            return cursor.fetchone()


    def create_order_fullinfo(self, order_info, connection):
        """ [서비스] 결제버튼 누를 시 order 테이블에 추가
        Author:
            Ji Yoon Lee
        Args:
            order_info(dict)
        Returns:
            추가된 order_id
        Note:
            이 로직으로 들어오는 오더는 결제완료된 오더이므로 order_statys_type_id = 2로 고정
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
        """ [서비스] order 테이블에 변화가 생길때 기록하는 log 테이블 추가 로직
        Author:
            Ji Yoon Lee
        Args:
            order_info(dict)
        Returns:
            추가된 로그테이블 order_log_id
        """
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
            WHERE o.id = %(order_id)s
            """
            cursor.execute(query, order_info)
            return cursor.lastrowid

    def patch_cart(self, order_info, connection):
        """ [서비스] 결제시 개별 상품(카트) 업데이트
        Author:
            Ji Yoon Lee
        Args:
            order_info(dict)
        Returns:
            추가된 배송지 address_id
        Note:
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
            #1 = 장바구니, 2 = 결제, 3 = 바로결제 시도, 4 = 배송중, 5 = 확정대기, 6 = 취소, 7 = 환불
            cursor.execute(query, order_info)
            return True
