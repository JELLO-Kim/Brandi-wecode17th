from model.mypage_dao   import MyPageDao
from flask              import jsonify, json
from errors             import *

class MyPageService:

    def mypage_qna(self, connection, user_id, page_condition, answer):
        mypage_dao = MyPageDao()
        mypage_qna = mypage_dao.mypyage_qna_dao(connection, user_id, page_condition, answer)

        result = []
        for i in mypage_qna:
            a = {}
            a['id'] = i['id']
            a['username'] = i['username']
            a['contents'] = i['contents']
            a['category'] = i['category']
            a['created_at'] = i['created_at']
            # 답변이 있는경우 answer에 담아줌
            if i['answer_id']:
                a['answer'] = {
                    'id': i['answer_id'],
                    'replier': i['answer_replier'],
                    'content': i['answer_content'],
                    'created_at': i['answer_time'],
                    'parent_id': i['answer_parent']
                }
            result.append(a)
        return {"data" : result}