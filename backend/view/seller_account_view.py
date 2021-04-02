from flask          import request, Blueprint
from db_connector   import connect_db
from service        import SellerService
from errors         import *
from utils          import login_decorator

class SellerView:
    seller_app = Blueprint('seller_app', __name__, url_prefix='/seller')

    @seller_app.route('/edit', methods=['GET'])
    @login_decorator
    def seller_edit():
        connection = None
        try:
            user_id = g.token_info['user_id']
            connection = connect_db()

            seller_service = SellerService()
            result = seller_service.seller_edit_get(user_id, connection)
            return {"data" : result}
        except ApiException as e:
            if connection:
                connect.rollback()
            raise e

        finally:
            if connection:
                connection.close()

        return {"data" : result}

    @seller_app.route('/edit', methods=['PATCH'])
    @login_decorator
    def seller_account():
        connection = None
        try:
            user_id = g.token_info['user_id']
            data = request.get_json()
            connection = connect_db()
            manager = data['manager']
            for one_manager in manager:
                one = {
                    "name" : one_manager['name'],
                    "email" : one_manager['email']
                }

            seller_edit_info = {
                'profile'               : data.get('profile', None),
                'background_image'      : data.get('backgroundImage', None),
                'introduce'             : data.get('introduce', None),
                'description'           : data.get('detailDescription', None),
                'manager'               : data.get('manager', None),
                'call_number'           : data.get('callNumber', None),
                'call_name'             : data.get('callName', None),
                'call_start'            : data.get('callStart', None),
                'call_end'              : data.get('callEnd', None),
                'postal_code'           : data.get('postal', None),
                'address'               : data.get('address', None),
                'detail_address'        : data.get('detailAddress', None),
                'delivery_info'         : data.get('shippingDescription', None),
                'refund_info'           : data.get('orderDescription', None),
                'is_weekend'            : data.get('isWeekend', None),
                'managers'              : data.get('managers', None)
            }

            seller_service = SellerService()
            result = seller_service.seller_edit_service(user_id, seller_edit_info, connection)

            connection.commit()
            return {"data" : result}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @seller_app.route('/edit', methods=['DELETE'])
    @login_decorator
    def seller_delete():
        connection = None
        try:
            user_id = g.token_info['user_id']
            connection = connect_db()
            data = response.json()
            manager_id = data['managerId']

            seller_service = SellerService()
            result = seller_service.seller_edit_delete(user_id, connection)
            return {"data" : result}
        except ApiException as e:
            if connection:
                connect.rollback()
            raise e

        finally:
            if connection:
                connection.close()

        return {"data" : result}

        
        