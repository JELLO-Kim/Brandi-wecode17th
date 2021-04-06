from flask          import request, Blueprint, jsonify, g
from db_connector   import connect_db
from service        import MyPageService
from responses      import *
from utils          import *

class MyPageView:
    mypage_app = Blueprint('mypage_app', __name__, url_prefix='/mypage')
    @mypage_app.route('/qna', methods=['GET'])
    @login_decorator
    def mypage_qna():
        """ 로그인 user의 마이페이지 - QNA list 확인
        Author:  
            Chae hyun Kim
        Args:  
            - token(str) : 로그인 user의 토큰
            - limit & offset(str) : 값이 들어오지 않을경우 limit 5와 offset 0으로 지정, int형으로 변환
            - answer(str) : 들어오지 않을경우 "전체", 0 = 미답변, 1 = 답변된 Question list+Answer를 지정해줄 조건
        Returns: 
            - 200: { "message"   : "SUCCESS"
                     "result"    : {
                        "data"          : user가 작성한 qna list,
                        "totalCount"    : qna 갯수}
                    }
        Note:    
            - filtering 조건에 따른 로그인 user의 QNA list 반환
        """
        connection = None
        page_condition  = {}
        user = {
            "user_id" : g.token_info['user_id'],
            "user_type_id" : g.token_info['user_type_id']
        }
        limit           = request.args.get('limit', None)
        offset          = request.args.get('offset', None)
        qna_answer      = request.args.get('answer', None)

        #limit 조건의 경우 횟수와 상관없이 언제나 5개의 값이 지정됨
        if limit is None:
            page_condition['limit'] = 5
        else:
            page_condition['limit'] = (limit)
        #offset 조건의 경우 값이 입력되지 않았을 경우 0이 지정됨
        if offset is None:
            page_condition['offset'] = 0
        else:
            page_condition['offset'] = (offset)

        #답변/미답변 선택하여 필터링 조건이 들어올 시 해당 값을 page_condition의 answer 키값에 저장
        page_condition['answer'] = qna_answer

        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            user_qna_list   = mypage_service.mypage_qna(connection, user, page_condition)
            return user_qna_list
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
        """ 로그인 user의 마이페이지 - 결제완료된 주문내역 list 
        Author:
            Chae hyun Kim
        Args:  
            - token(str) : 로그인 user의 토큰
            - limit & offset(str) : 값이 들어오지 않을경우 limit 5와 offset 0으로 지정, int형으로 변환
        Returns:
            - 200 : { "message"   : "SUCCESS"
                      "result"    : {
                            "data"          : user가 결제완료한 order list,
                            "totalCount"    : 주문내역 갯수(한 주문번호당 1개)
                            }
                    }
        Note
            : 결제 완료한 항목에 한해서 결과 반환
        """
        connection = None
        page_condition = {}
        user = {
            "user_id" : g.token_info['user_id'],
            "user_type_id" : g.token_info['user_type_id']
        }
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
            extra           = mypage_service.mypage_order(connection, user, page_condition)
            return extra
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @mypage_app.route('/order/<int:order_id>', methods=['GET'])
    @login_decorator
    def mypage_order_detail(order_id):
        """ 로그인 user의 마이페이지 - order 한 건에 대한 상세 내용 확인
        Author:  
            Chae hyun Kim
        Args:    
            - token(str)    : 로그인 user의 token
            - order_id(int) : 상세로 확인할 주문내역의 pk값(id)
        Returns:
            - 200 : { "message"   : "SUCCESS"
                      "result"    : {
                            "data"  : user가 결제한 order 한건에 대한 상세 내용
                            }
                    }
            - 400 : NOT FOUND 잘못된 path parameter 접근시
        """
        user = {
            "user_id" : g.token_info['user_id'],
            "user_type_id" : g.token_info['user_type_id']
        }
        connection = None
        try:
            connection      = connect_db()
            mypage_service  = MyPageService()
            result          = mypage_service.mypage_order_detail(connection, user, order_id)
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @mypage_app.route('/order', methods=['DELETE'])
    @login_decorator
    def mypage_order_delete(order_id):
        """ 로그인 user의 마이페이지 - order 한건 삭제
        Author:
            Chae hyun Kim
        Args:
            - token(str) : 로그인 user의 token
            - order_id(int) : request.body에 담겨져 들어올 배열 형태의 id
        Returns: 
            - 200 : { "message"   : "삭제되었습니다"
                      "result"    : "DELETE"
                    }
        """
        user_id = g.token_info['user_id']
        connection = None
        try:
            connection      = connect_db()
            data            = response.json()
            order_id        = data['id']
            mypage_service  = MyPageService()
            extra           = mypage_service.mypage_order_delete(connection, user_id, order_id)
            connection.commit()
            return {"custom_message" : DELETED, "result" : "DELETE"}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()
