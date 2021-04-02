import pymysql

class OrderDao:
    
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
            REPLACE INTO carts(
                order_id,
                cart_status_type_id
            ) VALUES (
                %(order_id)s,
                1
            )
            WHERE id = %(cart_id)s
            """
            #1 = 확정대기
            cursor.execute(cart, cart_info)
            return cursor.lastrowid