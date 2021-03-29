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

            if 'answer' in answer:
                status = answer['answer']
                print('???????????????', status)
                q_info += """
                    AND
                        q.is_finished = %(status)s
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
            cursor.execute(q_info, {'user_id' : user_id, 'status' : status})
            q_list = cursor.fetchall()
            return q_list