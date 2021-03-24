from flask import request, Blueprint, jsonify
from db_connector import connect_db
from exceptions import *
from service.order_service import OrderService
from utils import login_decorator

class OrderView():
    order_app = Blueprint('order_app', __name__)

    @order_app.route('/cart', methods=['POST'])
  #  @login_decorator
    def post_cart():
        connection = None
        try:
            data = request.json
            user_id = request.headers.get("user_id")

            if 'products' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'product_id' not in data:
                raise ApiException(400, INVALID_INPUT)
            for product in data['products']:
                if 'color' not in product:
                    raise ApiException(400, INVALID_INPUT)
                if 'size' not in product:
                    raise ApiException(400, INVALID_INPUT)
                if 'quantity' not in product:
                    raise ApiException(400, INVALID_INPUT)
                if 'price' not in product:
                    raise ApiException(400, INVALID_INPUT)

            order_info = {
                'product_id': data['product_id'],
                'products': data['products'],
                'user_id': user_id
            }

            connection = connect_db()
            order_service = OrderService()
            order_service.post_cart(order_info, connection)
            connection.commit()

            return jsonify({'MESSAGE': CREATED}), 201

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

