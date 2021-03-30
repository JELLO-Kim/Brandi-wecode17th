from flask          import request, Blueprint, g
from db_connector   import connect_db
from service        import MyPageService
from errors         import *
from utils          import login_decorator

class MyPageView:
    mypage_app = Blueprint('mypage_app', __name__, url_prefix='/mypage')
    @mypage_app.route('/qna', methods=['GET'])
    @login_decorator
    def mypage_qna():
        page_condition  = {}
        answer          = {}
        user_id         = g.token_info['user_id']
        limit           = request.args.get('limit', None)
        offset          = request.args.get('offset', None)
        qna_answer      = request.args.get('answer', None)

        if limit is None:
            page_condition['limit'] = 5
        else:
            page_condition['limit'] = int(limit)

        #limit 조건의 경우 횟수와 상관없이 언제나 5개의 값이 지정됨
        if offset is None:
            page_condition['offset'] = 0
        else:
            page_condition['offset'] = int(offset)

        #답변/미답변 선택하여 필터링 조건이 들어올 시 해당 값을 dict 형태로 변환
        if qna_answer is not None:
            answer['answer'] = int(qna_answer)

        connection = None
        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            result          = mypage_service.mypage_qna(connection, user_id, page_condition, answer)
            return result
        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection is not None:
                connection.close

    @mypage_app.route('/order', methods=['GET'])
    @login_decorator
    def mypage_order():
        page_condition = {}
        user_id = g.token_info['user_id']
        limit   = request.args.get('limit', None)
        offset  = request.args.get('offset', None)

        if limit is None:
            page_condition['limit'] = 5
        else:
            page_condition['limit'] = int(limit)
        if offset is None:
            page_condition['offset'] = 0
        else:
            page_condition['offset'] = int(offset)

        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            result           = mypage_service.mypage_order(connection, user_id, page_condition)
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @mypage_app.route('/order/<order_id>', methods=['GET'])
    # @login_decorator
    def mypage_order_detail(order_id):
        user_id = g.token_info['user_id']
        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            result           = mypage_service.mypage_order_detail(connection, user_id, order_id)
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()