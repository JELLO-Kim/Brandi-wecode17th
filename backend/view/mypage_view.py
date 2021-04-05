from flask          import request, Blueprint, jsonify
from db_connector   import connect_db
from service        import MyPageService
from responses      import *
from utils          import *

class MyPageView:
    mypage_app = Blueprint('mypage_app', __name__, url_prefix='/mypage')
    @mypage_app.route('/qna', methods=['GET'])
    def mypage_qna():
        """ 로그인 user의 마이페이지 - QNA list 확인
        Author  
            : Chae hyun Kim
        Args    
            : token
            : limit & offset - 값이 들어오지 않을경우 limit 5와 offset 0으로 지정
        Returns 
            : { "message"   : "SUCCESS"
                "result"    : {
                    "data"          : user가 작성한 qna list,
                    "totalCount"    : qna 갯수}
                }
        Note    
            : filtering 조건으로 category의 id가 query parameter를 통해 들어올 경우 해당 조건에 해당하는 product list로 결과 반환
        """
        connection = None
        page_condition  = {}
        user_id         = 3
        limit           = request.args.get('limit', None)
        offset          = request.args.get('offset', None)
        qna_answer      = request.args.get('answer', None)

        #limit 조건의 경우 횟수와 상관없이 언제나 5개의 값이 지정됨
        if limit is None:
            page_condition['limit'] = 5
        else:
            page_condition['limit'] = int(limit)
        #offset 조건의 경우 값이 입력되지 않았을 경우 0이 지정됨
        if offset is None:
            page_condition['offset'] = 0
        else:
            page_condition['offset'] = int(offset)

        #답변/미답변 선택하여 필터링 조건이 들어올 시 해당 값을 page_condition의 answer 키값에 저장
        if qna_answer is not None:
            page_condition['answer'] = int(qna_answer)

        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            user_qna_list   = mypage_service.mypage_qna(connection, user_id, page_condition)
            return user_qna_list
        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection is not None:
                connection.close
                
    @login_decorator
    @mypage_app.route('/order', methods=['GET'])
    def mypage_order():
        """ 로그인 user의 마이페이지 - order list 확인
        Author  
            : Chae hyun Kim
        Args    
            : token
            : limit & offset - 값이 들어오지 않을경우 limit 5와 offset 0으로 지정
        Returns 
            : { "message"   : "SUCCESS"
                "result"    : {
                    "data"          : user가 결제한 order list,
                    "totalCount"    : 주문내역 갯수(한 주문번호당 1개)}
                }
        Note
            : 결제 완료한 항목에 한해서 결과 반환
        """
        connection = None
        page_condition = {}

        # user_id = request.headers['Authorization']
        user_id = 3
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
            extra           = mypage_service.mypage_order(connection, user_id, page_condition)
            return extra
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @mypage_app.route('/order/<order_id>', methods=['GET'])
    @login_decorator
    def mypage_order_detail(order_id):
        """ 로그인 user의 마이페이지 - order 한 건에 대한 상세 내용 확인
        Author  
            : Chae hyun Kim
        Args:    
            user_id : 로그인 유저의 token으로부터 받는 id
            order_id : 상세로 확인할 주문내역의 pk값(id)
        Returns 
            : { "message"   : "SUCCESS"
                "result"    : {
                    "data"  : user가 결제한 order 한건에 대한 상세 내용
                    }
                }
        """
        user_id = g.token_info['user_id']
        connection = None
        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            result          = mypage_service.mypage_order_detail(connection, user_id, order_id)
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @mypage_app.route('/order', methods=['DELETE'])
    def mypage_order_delete(order_id):
        """ 로그인 user의 마이페이지 - order 한건 삭제
        Author  
            : Chae hyun Kim
        Args    
            : token
            : order_id
        Returns 
            : { "message"   : "SUCCESS"
                "result"    : {
                    "message"  : "삭제되었습니다"
                    }
                }
        """
        user_id = request.headers['Authorization']
        connection = None
        try:
            connection      = connect_db()
            data            = response.json()
            order_id        = data['id']
            mypage_service  = MyPageService()
            extra           = mypage_service.mypage_order_delete(connection, user_id, order_id)
            connection.commit()
            return jsonify({"message" : DELETED})
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()
