import pymysql

from flask import jsonify
from responses import *

class MyPageDao:
    def mypyage_qna_dao(self, connection, user, page_condition):
        """ [서비스] 로그인 유저의 mypage - qna list
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id에 대한 정보가 들어있는 dict
            - page_condition(dict) : limit, offset, filtering 조건에 필요한 answer에 대한 정보가 들어있는 dict
        Returns 
            : q_list = 로그인 유저의 질문과 답변 list
        """
        limit = page_condition['limit']
        offset = page_condition['offset']

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 질문 목록들 (parent_id가 NULL인것들)
            q_info = """
                SELECT
                    q.id,
                    qt.name AS category,
                    q.is_finished AS isFinished,
                    u.username,
                    q.created_at,
                    q.contents,
                    qna_r.id AS answer_id,
                    qna_r.created_at AS answer_time,
                    qna_r.contents AS answer_contents,
                    qna_r.parent_id AS answer_parent,
                    seller.username AS answer_replier
                FROM
                    qnas AS q
                    LEFT JOIN qnas AS qna_r
                        ON q.id = qna_r.parent_id
                    LEFT JOIN user_info AS seller
                        ON qna_r.replier_id = seller.id
                    JOIN user_info AS u
                        ON q.writer_id = u.id
                    JOIN question_types AS qt
                        ON q.question_type_id=qt.id
                WHERE
                    q.is_delete = 0
                    AND
                        u.id = %(user_id)s
                    AND
                        q.parent_id is NULL
                """
            # 답변/미답변 필터링 조건 존재 시
            if page_condition['answer']:
                q_info += """
                    AND
                        q.is_finished = %(answer)s
                    """
            q_info += """
                ORDER BY
                    q.id          
                """

            # 질문 목록에 대한 limit & offset 설정
            q_info += f"""
                LIMIT {limit}
                OFFSET {offset}
            """

            cursor.execute(q_info, {'user_id' : user['user_id'], 'answer' : page_condition['answer']})
            q_list = cursor.fetchall()
          
            return q_list

    def mypage_qna_count(self, connection, user, page_condition):
        """ [서비스] 로그인 유저의 mypage - qna 갯수 파악
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user : 로그인 유저의 user_id, user_type_id에 대한 정보가 들어있는 dict
            - page_condition : filtering 조건에 필요한 answer에 대한 정보가 들어있는 dict
        Returns:
            - q_counting = filtering 조건에 맞는 로그인 유저의 질문갯수
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:            
            q_count = """
                SELECT
                    COUNT(*)
                FROM
                    qnas AS q
                    LEFT JOIN qnas AS qna_r
                        ON q.id = qna_r.parent_id
                    LEFT JOIN user_info AS seller
                        ON qna_r.replier_id = seller.id
                    JOIN user_info AS u
                        ON q.writer_id = u.id
                    JOIN question_types AS qt
                        ON q.question_type_id=qt.id
                WHERE
                    q.is_delete = 0
                    AND
                        u.id = %(user_id)s
                    AND
                        q.parent_id is NULL
                """
            # 답변/미답변 필터링 조건 존재 시
            if page_condition['answer']:
                q_count += """
                    AND
                        q.is_finished = %(answer)s
                    """
            cursor.execute(q_count, {'user_id' : user['user_id'], 'answer' : page_condition['answer']})
            q_counting = cursor.fetchall()

            return q_counting



    def mypage_order_header_dao(self, connection, user, page_condition):
        """ [서비스] 로그인 유저의 mypage - 주문 번호 파악
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id에 대한 정보가 들어있는 dict
            - page_condition(dict) : limit, offset에 대한 정보가 들어있는 dict
        Returns:
            - order_header_list =  로그인 유저의 결제완료된 주문 번호 list (주분번호와 주문시간, 외부용 주문번호 반환)
        """
        limit = page_condition['limit']
        offset = page_condition['offset']
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            limit = page_condition['limit']
            offset = page_condition['offset']
            order_header_info = """
                SELECT
                    o.id,
                    o.created_at,
                    o.order_number AS orderNumber
                FROM
                    orders AS o
                WHERE
                    o.is_delete = 0
                    AND
                    o.user_id = %(user_id)s
                    AND
                    o.order_status_type_id = 2
                """

            order_header_info += f"""
                LIMIT {limit}
                OFFSET {offset}
            """
            cursor.execute(order_header_info, {'user_id' : user['user_id']})
            order_header_list = cursor.fetchall()
            return order_header_list


    def mypage_order_cart_dao(self, connection, user, page_condition, order_id):
        """ [서비스] 로그인 유저의 mypage - n건의 주문 번호에 해당하는 상품 옵션들 반환
        Author : Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id에 대한 정보가 담긴 dict
            - order_id(int) : 주문번호의 pk값(id)
        Returns:
            - 로그인 유저의 주문 내역 list (주문번호에 해당되는 상품옵션들 반환)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            order_info = """
                SELECT
                    c.id,
                    p.name,
                    color.name AS productColor,
                    size.name AS productSize,
                    c.calculated_price AS totalPrice,
                    p.discount_rate AS discountRate,
                    p.discountPrice AS onePrice,
                    cs.name AS status,
                    c.quantity,
                    p.id AS productId,
                    c.cart_number AS cartNumber,
                    c.order_id AS orderId,
                    o.order_number AS orderNumber,
                    s.korean_brand_name AS brand,
                    s.user_info_id AS sellerId,
                    c.order_id AS cartOrderId,
                    pt.image_url AS productImage
                FROM
                    carts AS c
                JOIN
                    orders AS o
                ON
                    c.order_id = o.id
                JOIN
                    cart_status_types AS cs
                ON
                    c.cart_status_type_id = cs.id
                LEFT JOIN
                    product_options AS po
                ON
                    c.product_option_id = po.id
                JOIN
                    products AS p
                ON
                    po.product_id = p.id
                JOIN
                    product_thumbnails AS pt
                ON
                    pt.product_id = p.id
                JOIN
                    sellers AS s
                ON
                    p.seller_id = s.user_info_id
                JOIN
                    product_size_types AS size
                ON
                    po.product_size_type_id = size.id
                JOIN
                    product_color_types AS color
                ON
                    po.product_color_type_id = color.id
                WHERE
                    o.user_id = %(user_id)s
                    AND
                    c.order_id IN %(order_id)s
                    AND
                    pt.ordering = 1
            """

            cursor.execute(order_info, {'user_id' : user['user_id'], 'order_id' : order_id})
            order_list = cursor.fetchall()
            return order_list

    def mypage_order_count(self, connection, user):
        """ [서비스] 로그인 유저의 mypage - n건의 주문 번호 갯수 파악
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id에 대한 정보가 담긴 dict
        Returns:
            - 로그인 유저의 주문 내역 갯수 반환
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            order_count = """
                SELECT
                    COUNT(*)
                FROM
                    orders AS o
                WHERE
                    o.is_delete = 0
                AND
                    o.user_id = %(user_id)s
                """
            cursor.execute(order_count, {'user_id' : user['user_id']})
            order_counting = cursor.fetchall()

            return order_counting

    def mypage_order_detail_header_dao(self, connection, user, order_id):
        """ [서비스] 로그인 유저의 mypage - 주문내역 1건에 대한 상세 내용
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id 에 대한 정보가 담긴 dict
            - order_id(int) : 주문번호의 pk값(id)
        Returns:
            - {
                "detailHeader" : order_detail_header = 결제완료된 주문번호,
                "detailProducts" : order_detail_list = 주문번호에 해당하는 상품옵션들
              }
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            order_detail_header = """
                SELECT
                    o.id,
                    o.order_number,
                    o.created_at,
                    o.order_name,
                    o.total_price,
                    os.name,
                    u.phone_number,
                    s.recipient_address AS address,
                    sm.contents,
                    o.is_delete
                FROM
                    orders AS o
                JOIN
                    user_info AS u
                ON
                    o.user_id = u.id
                JOIN
                    order_status_types AS os
                ON
                    o.order_status_type_id = os.id
                JOIN
                    shipping_info AS s
                ON
                    o.shipping_info_id = s.id
                JOIN
                    shipping_memo_types AS sm
                ON
                    o.shipping_memo_type_id = sm.id
                WHERE
                    o.id = %(order_id)s
                    AND
                    o.is_delete = 0
                """
            
            order_detail_products = """
                SELECT
                    c.id,
                    s.korean_brand_name AS brand,
                    p.name,
                    color.name AS productColor,
                    size.name AS prodcutSize,
                    c.quantity,
                    c.calculated_price AS totalPrice,
                    pt.image_url AS image
                    
                FROM
                    carts AS c
                JOIN
                    product_options AS po
                ON
                    c.product_option_id = po.id
                JOIN
                    products AS p
                ON
                    po.product_id = p.id
                JOIN
                    product_thumbnails AS pt
                ON
                    pt.product_id = p.id
                JOIN
                    product_size_types AS size
                ON
                    po.product_size_type_id = size.id
                JOIN
                    product_color_types AS color
                ON
                    po.product_color_type_id = color.id
                JOIN
                    sellers AS s
                ON
                    p.seller_id = s.user_info_id
                WHERE
                    c.order_id = %(order_id)s
                    AND
                    pt.ordering = 1
                """

            cursor.execute(order_detail_header, {'user_id' : user['user_id'], 'order_id' : order_id})
            order_detail_header = cursor.fetchone()

            if order_detail_header['is_delete'] == 1:
                raise ApiException(404, PAGE_NOT_FOUND)

            cursor.execute(order_detail_products, {'user_id' : user['user_id'], 'order_id' : order_id})
            order_detail_list = cursor.fetchall()

            return {"detailHeader" : order_detail_header, "detailProducts" : order_detail_list}

    def detail_shipping_info(self, connection, order_id):
        """ [서비스] 로그인 유저의 mypage - 주문내역 1건에 대한 배송지 정보
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id에 대한 정보가 담긴 dict
            - order_id : 주문번호의 pk값(id)
        Returns:
            - 주문내역 한건에 대한 배송지 정보 반환
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            shipping_query = """
                SELECT
                    s.recipient_name AS name,
                    s.recipient_phone AS phone,
                    s.recipient_postal_code AS postal,
                    s.recipient_address AS address,
                    s.recipient_address_detail AS detailAddress,
                    sm.contents
                FROM
                    shipping_info AS s
                LEFT JOIN
                    orders AS o
                    ON
                    o.shipping_info_id = s.id
                INNER JOIN
                    shipping_memo_types AS sm
                    ON
                    o.shipping_memo_type_id = sm.id
                WHERE
                    o.id = %(order_id)s
                """
            cursor.execute(shipping_query, {"order_id" : order_id})

            return cursor.fetchone()

    def order_detail_cart_count(self, connection, order_id):
        """ [서비스] 로그인 유저의 mypage - 주문내역 1건에 해당되는 상품옵션 갯수 반환
        Author:
            Chae hyun Kim
        Args:
            - connection : 커넥션
            - user(dict) : 로그인 유저의 user_id, user_type_id에 대한 정보가 담긴 dict
            - order_id(int) : 주문번호의 pk값(id)
        Returns 
            : 주문내역 한건에 해당하는 상품 옵션 갯수 반환
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            count_query = """
                SELECT
                    COUNT(*)
                FROM
                    carts AS c
                JOIN
                    product_options AS po
                ON
                    c.product_option_id = po.id
                JOIN
                    products AS p
                ON
                    po.product_id = p.id
                JOIN
                    product_thumbnails AS pt
                ON
                    pt.product_id = p.id
                JOIN
                    product_size_types AS size
                ON
                    po.product_size_type_id = size.id
                JOIN
                    product_color_types AS color
                ON
                    po.product_color_type_id = color.id
                JOIN
                    sellers AS s
                ON
                    p.seller_id = s.user_info_id
                WHERE
                    c.order_id = %(order_id)s
                    AND
                    pt.ordering = 1
                """
            cursor.execute(count_query, {"order_id" : order_id})

            return cursor.fetchone()