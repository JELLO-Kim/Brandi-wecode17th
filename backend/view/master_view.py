from flask        import request, Blueprint, jsonify
from db_connector import connect_db
from service      import MasterService
from responses    import *
from utils        import login_decorator

class MasterView:

    master_app = Blueprint('master_app', __name__, url_prefix='/master')

    # @login_decorator
    @master_app.route('/account', methods=['GET'])
    def master_account():
        # 로그인 했을 때 3(마스터)인지 확인
        # if g.token_info['user_type_id'] != 3:
        #     raise ApiException(400, USER_NOT_MASTER)

        # 페이지에 대한 조건들을 담은 객체
        page_condition  = {}
        limit           = request.args.get('limit', None)
        offset          = request.args.get('offset', None)

        # 한 페이지당 데이터 갯수는 기본 10개로 설정.
        if limit is None:
            page_condition['limit'] = 10
        else:
            page_condition['limit'] = int(limit)

        # 페이지 시작은 0부터 시작함.
        if offset is None:
            page_condition['offset'] = 0
        else:
            page_condition['offset'] = int(offset)

        # 입력창에 입력한 조건들을 담은 객체
        filters   = {
            'no'               : request.args.get('no', None),
            'username'         : request.args.get('username', None),
            'english'          : request.args.get('english', None),
            'korean'           : request.args.get('koean', None),
            'seller_type'      : request.args.get('sellerType', None), # id값으로 넘어온다.
            'seller_status'    : request.args.get('sellerStatus', None), # id값으로 넘어온다.
            'seller_attribute' : request.args.get('sellerAttribute', None), # id값으로 넘어온다.
            'manager_name'     : request.args.get('managerName', None),
            'manager_phone'    : request.args.get('managerPhone', None),
            'manager_email'    : request.args.get('managerEmail', None),
            'start_date'       : request.args.get('startDate', None), # type = date
            'end_date'         : request.args.get('endDate', None), # type = date
        }

        connection = None

        try:
            connection      = connect_db()
            master_service  = MasterService()
            result          = master_service.account(connection, page_condition, filters)

            return result
        except Exception as e:
            if connection:
                connection.rollback

            raise e
        finally:
            if connection is not None:
                connection.close
    
    # @login_decorator
    @master_app.route('/account/init', methods=['GET'])
    def master_account_init():
        # 로그인 했을 때 3(마스터)인지 확인
        # if g.token_info['user_type_id'] != 3:
        #     raise ApiException(400, USER_NOT_MASTER)

        connection = None

        try:
            connection      = connect_db()
            master_service  = MasterService()
            result          = master_service.account_init(connection)

            return result
        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection is not None:
                connection.close
    
    # @login_decorator
    @master_app.route('/account/level', methods=['PATCH'])
    def account_level():
        # 로그인 했을 때 3(마스터)인지 확인
        # if g.token_info['user_type_id'] != 3:
        #     raise ApiException(400, USER_NOT_MASTER)

        data = {
            # 'user_id'   : g.token_info['user_id'],
            'user_id'   : 1,
            'action_id' : request.args.get('action_id', None)
        }
        
        connection = None

        try:
            connection     = connect_db()
            master_service = MasterService()
            result         = master_service.account_level(connection, data)

            if result: connection.commit()

            return result
        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection is not None:
                connection.close 
    