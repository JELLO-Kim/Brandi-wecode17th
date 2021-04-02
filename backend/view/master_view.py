from flask          import request, Blueprint, jsonify
from db_connector   import connect_db
from service        import MasterService
from responses         import *

class MasterView:

    master_app = Blueprint('master_app', __name__, url_prefix='/master')

    @master_app.route('/account', methods=['GET'])
    def master_account_app():
        page_condition  = {}
        user_id         = request.headers['Authorization']
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

        connection = None
        try:
            connection      = connect_db()
            master_service  = MasterService()
            result          = master_service.account(connection, page_condition)
            return result
        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection is not None:
                connection.close