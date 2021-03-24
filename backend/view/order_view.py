from flask import request, Blueprint, jsonify, g
from db_connector import connect_db
from exceptions import *
from service.order_service import OrderService
from utils import login_decorator

class OrderView():
    order_app = Blueprint('order_app', __name__)

    @order_app.route('/cart', methods=['POST'])
    @login_decorator
    def post_cart():
        connection = None
        try:
            data = request.json
            user_id = g.token_info['user_id']
            products = data['products']

            if 'products' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'productId' not in data:
                raise ApiException(400, INVALID_INPUT)
            for product in products:
                if 'color' not in product:
                    raise ApiException(400, COLOR_NOT_IN_INPUT)
                if 'size' not in product:
                    raise ApiException(400, SIZE_NOT_IN_INPUT)
                if 'quantity' not in product:
                    raise ApiException(400, QUANTITY_NOT_IN_INPUT)
                if 'price' not in product:
                    raise ApiException(400, PRICE_NOT_IN_INPUT)

            order_info = {
                'user_id': user_id,
                'product_id': data['productId']
            }

            connection = connect_db()
            order_service = OrderService()
            order_service.post_cart(order_info, products, connection)
            connection.commit()

            return jsonify({'MESSAGE': CREATED}), 201

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @order_app.route('/cart', methods=['GET'])
    @login_decorator
    def get_cart():
        user_id = g.token_info['user_id']
        order_info = {'user_id': user_id}
        connection = connect_db()
        order_service = OrderService()
        cart_details = order_service.get_cart(order_info, connection)

        return jsonify({'RESULTS': cart_details}), 200

    @order_app.route('/cart/<int:productId>', methods=['POST'])
    @login_decorator
    def delete_cart(productId):
        user_id = g.token_info['user_id']
        connection = None
        try:
            data = request.json
            if 'color' not in data:
                raise ApiException(400, COLOR_NOT_IN_INPUT)
            if 'size' not in data:
                raise ApiException(400, SIZE_NOT_IN_INPUT)
            order_info = {
                'user_id': user_id,
                'product_id': productId,
                'color': data['color'],
                'size': data['size']
            }
            connection = connect_db()
            order_service = OrderService()
            order_service.delete_cart(order_info, connection)
            connection.commit()

            return jsonify({'MESSAGE': OK}), 200

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()