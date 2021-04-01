import pymysql

from flask import jsonify
from errors import *

class MyPageDao:
    def mypyage_qna_dao(self, connection, user_id, page_condition, answer):
        limit = page_condition['limit']
        offset = page_condition['offset']

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 질문 목록들 (parent_id가 NULL인것들)
            q_info = """
                SELECT
                    q.id,
                    qt.name AS category,
                    q.is_finished,
                    u.username,
                    q.created_at,
                    q.contents,
                    qna_r.id AS answer_id,
                    qna_r.created_at AS answer_time,
                    qna_r.contents AS answer_content,
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
            if 'answer' in answer:
                answer = answer['answer']
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

            cursor.execute(q_info, {'user_id' : user_id, 'answer' : answer})
            q_list = cursor.fetchall()
          
            return q_list

    def mypage_qna_count(self, connection, user_id, answer):
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
            if 'answer' in answer:
                answer = answer['answer']
                q_count += """
                    AND
                        q.is_finished = %(answer)s
                    """
            cursor.execute(q_count, {'user_id' : user_id, 'answer' : answer})
            q_counting = cursor.fetchall()

            return q_counting



    def mypage_order_header_dao(self, connection, user_id, page_condition):
        limit = page_condition['limit']
        offset = page_condition['offset']
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            order_header_info = """
                SELECT
                    o.id,
                    o.created_at,
                    o.order_number
                FROM
                    orders AS o
                WHERE
                    o.is_delete = 0
                AND
                    o.user_id = %(user_id)s
                """

            order_header_info += f"""
                LIMIT {limit}
                OFFSET {offset}
            """
            cursor.execute(order_header_info, {'user_id' : user_id})
            order_header_list = cursor.fetchall()

            return order_header_list


    def mypage_order_cart_dao(self, connection, user_id, page_condition, order_id):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            order_info = """
                SELECT
                    c.id,
                    p.name,
                    color.name,
                    size.name,
                    c.quantity,
                    c.order_id,
                    o.order_number AS orderNumber,
                    s.korean_brand_name AS brand,
                    s.user_info_id AS sId,
                    c.order_id AS cartOrderId
                FROM
                    carts AS c
                JOIN
                    orders AS o
                ON
                    c.order_id = o.id
                LEFT JOIN
                    product_options AS po
                ON
                    c.product_option_id = po.id
                JOIN
                    products AS p
                ON
                    po.product_id = p.id
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
            """

            cursor.execute(order_info, {'user_id' : user_id, 'order_id' : order_id})
            order_list = cursor.fetchall()
            return order_list

    def mypage_order_count(self, connection, user_id):
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
            cursor.execute(order_count, {'user_id' : user_id})
            order_counting = cursor.fetchall()

            return order_counting