from flask import request, Blueprint, g
from db_connector import connect_db
from service import MasterService, SellerService
from responses import *
from utils import login_decorator


class MasterView:
    master_app = Blueprint('master_app', __name__, url_prefix='/master')

    @master_app.route('/seller-information/<int:sellerId>', methods=['GET'])
    @login_decorator
    def master_seller_edit_get(sellerId):
        """ [어드민] master의 seller 정보 수정페이지 - 정보 확인
        Author:
            : Chae hyun Kim
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200 :  
                { "message"   : "SUCCESS",
                    "result"    : {
                        "data" : 입력된 상세 정보
                    }
                }
            - 403 : user_type_id가 1이나 2일 경우 "일반 유저는 접근 권한이 없습니다"
        Note
            : 회원가입 후 첫 수정페이지 입장 시 null 값이 존재함.
        """
        connection = None
        try:
            user_type_id = g.token_info['user_type_id']
            if user_type_id == 1:
                raise ApiException(403, SERVICE_USER_NO_ACCESS)
            if user_type_id == 2:
                raise ApiException(403, ACCESS_DENIED)

            user = {
                'user_id' : sellerId,
                'changer_id' : g.token_info['user_id'],
                'user_type_id' : g.token_info['user_type_id']
            }
            connection = connect_db()
            seller_service = SellerService()
            result = seller_service.seller_edit_get(user, connection)

            return {'data': result}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @master_app.route('/seller-information/<int:sellerId>', methods=['PATCH'])
    @login_decorator
    def master_seller_edit(sellerId):
        """ [어드민] master의 seller 정보 수정페이지 - 수정
        Author:
            Chae hyun Kim
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200 : { "message"   : "SUCCESS",
                        "result"    : {
                            "data" : 수정한 내역 갯수
                            }
                        }
            - 403 : user_type_id가 1이나 2일 경우 "일반 유저는 접근 권한이 없습니다"
        Note:
            - 추가 입력 정보에 대한 값은 들어오면 들어온 값으로, 들어오지 않는다면 해당 key에는 None을 담는다
        """
        connection = None
        try:
            user_type_id = g.token_info['user_type_id']
            if user_type_id == 1:
                raise ApiException(403, SERVICE_USER_NO_ACCESS)
            if user_type_id == 2:
                raise ApiException(403, ACCESS_DENIED)
            seller_service = SellerService()
            user = {
                'user_id' : sellerId,
                'changer_id' : g.token_info['user_id'],
                'user_type_id' : g.token_info['user_type_id']
            }
            connection = connect_db()
            data = request.get_json()

            seller_edit_info = {
                'profile'           : data.get('profile', None),
                'background_image'  : data.get('backgroundImage', None),
                'introduce'         : data.get('introduce', None),
                'description'       : data.get('description', None),
                'call_number'       : data.get('customerServicePhone', None),
                'callName'          : data.get('customerServiceName', None),
                'callStart'         : data.get('customerServiceOpen', None),
                'callEnd'           : data.get('customerServiceClose', None),
                'postalCode'        : data.get('postal', None),
                'address'           : data.get('address', None),
                'detailAddress'     : data.get('addressDetail', None),
                'delivery_info'     : data.get('deliveryInfo', None),
                'refund_info'       : data.get('refundInfo', None),
                'is_weekend'        : data.get('isWeekend', 0),
                'brandKorean'       : data.get('brandKorean', None),
                'brandEnglish'      : data.get('brandEnglish', None),
                'managers'          : data.get('managers', None)
            }

            seller_edit_info['user_id'] = str(user['user_id'])
            seller_service = SellerService()
            result = seller_service.seller_edit_service(user, seller_edit_info, connection)

            connection.commit()

            return {"custom_message" : UPDATED, "result" : "PATCH"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()


    @master_app.route('/account', methods=['GET'])
    @login_decorator
    def master_account():
        """ [어드민] 샐러 계정 관리(마스터)
        Author: 
            Sung joun Jang
        Args:    
            - limit: 페이지당 보여질 데이터 갯수
            - offset: 현재 페이지
            - no: 샐러의 no
            - username: 샐러 id
            - english: 브랜드의 영어 이름
            - korean: 브랜드의 한글 이름
            - sellerType: 샐러의 타입(일반, 헬피)
            - sellerStatus: 샐러의 상태(입점, 입점대기 등등)
            - sellerAttribute: 샐러의 속성(쇼핑몰, 뷰티 등등)
            - managerName: 매니저의 이름
            - managerPhone: 매니저의 핸드폰 번호
            - managerEmail: 매니저의 이메일
            - startDate: 샐러 생성된 날짜의 시작 값
            - endDate: 샐러 생성된 날짜의 끝 값
        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                    totalCount: 전체 데이터 개수
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        # 입력창에 입력한 조건들을 담은 객체
        filters = {
            'no': request.args.get('no', None),
            'username': request.args.get('username', None),
            'english': request.args.get('english', None),
            'korean': request.args.get('koean', None),
            'seller_type': request.args.get('sellerType', None), # id값으로 넘어온다.
            'seller_status': request.args.get('sellerStatus', None), # id값으로 넘어온다.
            'seller_attribute': request.args.get('sellerAttribute', None), # id값으로 넘어온다.
            'manager_name': request.args.get('managerName', None),
            'manager_phone': request.args.get('managerPhone', None),
            'manager_email': request.args.get('managerEmail', None),
            'start_date': request.args.get('startDate', None), # type = date
            'end_date': request.args.get('endDate', None), # type = date
        }

        # 페이지에 대한 조건들
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', None)

        # 한 페이지당 데이터 갯수는 기본 10개로 설정.
        if limit is None:
            filters['limit'] = 10
        else:
            filters['limit'] = int(limit)

        # 페이지 시작은 0부터 시작함.
        if offset is None:
            filters['offset'] = 0
        else:
            filters['offset'] = int(offset)

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.account(connection, filters)

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()

            raise e
        finally:
            if connection is not None:
                connection.close()

    @master_app.route('/account/init', methods=['GET'])
    @login_decorator
    def master_account_init():
        """ [어드민] 샐러 계정 관리(마스터) - 초기값
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.account_init(connection)

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()
    
    @master_app.route('/account/level', methods=['PATCH'])
    @login_decorator
    def account_level():
        """ [어드민] 샐러 계정 관리(마스터) - level 값 변경하기
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        body = request.json
        
        # 필수 request 값이 없으면 에러 return
        if not body.get('sellerId'):
            raise ApiException(400, NOT_SELLER)
        if not body.get('actionId'):
            raise ApiException(400, NOT_ACTION)

        seller_id = body['sellerId']
        action_id = body['actionId']

        data = {
            'user_id': g.token_info['user_id'],
            'seller_id': seller_id,
            'action_id': action_id
        }

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.account_level(connection, data)

            if result: connection.commit()

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @master_app.route('/order/ready/init', methods=['GET'])
    @login_decorator
    def order_ready_init():
        """ [어드민] 주문관리(마스터) - 상품준비(초기값)
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.order_ready_init(connection)

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @master_app.route('/order/ready', methods=['GET'])
    @login_decorator
    def order_ready():
        """ [어드민] 주문관리(마스터) - 상품준비(검색값)
        Author: 
            Sung joun Jang
        Args:    
            - categories: filter조건으로 들어오는 샐러 속성 값(리스트)
            - seachText: 검색창에 쓴 텍스트 값
            - searcgCategory: 검색 유형
            - limit: 한 페이지에 보여줄 데이터의 값
            - offset: 페이지에 대한 정보
        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        # 카테고리는 sql 'in'으로 검사하기 위해 튜플로 엮음
        filters = {
            'categories': tuple(request.args.getlist('categories')),
            'search_text': request.args.get('searchText'),
            'search_category': request.args.get('searchCategory')
        }

        # 페이지에 대한 조건들
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', None)

        # 한 페이지당 데이터 갯수는 기본 10개로 설정.
        if limit is None:
            filters['limit'] = 10
        else:
            filters['limit'] = int(limit)

        # 페이지 시작은 0부터 시작함.
        if offset is None:
            filters['offset'] = 0
        else:
            filters['offset'] = int(offset)

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.order_ready(connection, filters)

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @master_app.route('/order/ready/<int:cart_number>', methods=['PATCH'])
    @login_decorator
    def order_ready_update(cart_number):
        """ [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경)
        Author: 
            Sung joun Jang
        Args:    
            - cart_number: 변경하고자 하는 주문의 pk 값
        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        data = {
            'user_id': g.token_info['user_id'],
            'cart_number': cart_number
        }

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.order_ready_update(connection, data)

            connection.commit()

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()

    @master_app.route('/order/<cart_number>', methods=['GET'])
    @login_decorator
    def order_detail(cart_number):
        """ [어드민] 주문 상세 관리(마스터)
        Author: 
            Sung joun Jang
        Args:    
            - product_id: 조회하고자 하는 상품의 pk 값
            - cart_number: 조회하고자 하는 카트의 외부 고유 값
        Returns:
            - 200:
                message: 반환되는 메세지
                result: {
                    data: 전달하는 데이터 값
                }
        """
        # 로그인 했을 때 3(마스터)인지 확인
        if g.token_info['user_type_id'] != 3:
            raise ApiException(400, USER_NOT_MASTER)

        connection = None

        try:
            connection = connect_db()
            master_service = MasterService()
            result = master_service.order_detail(connection, cart_number)

            return {'result': result}
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()
