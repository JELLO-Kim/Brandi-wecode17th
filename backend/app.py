import json

from flask import Flask, jsonify, Response
from view import ProductView, MyPageView, UserView, OrderView, SellerView
from flask_cors import CORS
from flask.json import JSONEncoder
from decimal import Decimal
from datetime import datetime
from responses import *


class CustomJSONEncoder(JSONEncoder):
    """
        jsonify()를 사용하는데 몇몇 인코더가 필요한 부분이 있어서 obj : json 형태로 변환
        obj를 json형태로 변경하는 기능이 추가된 JSONEncoder
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        return JSONEncoder.default(self, obj)


def create_app(test_config=None):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_pyfile('config.py')
    app.register_blueprint(UserView.user_app)
    app.register_blueprint(OrderView.order_app)
    app.register_blueprint(SellerView.seller_app)
    # 모든 곳에서 호출하는 것을 허용
    CORS(app, resources={'*': {'origins': '*'}})

    # error 메세지 반환 from errors.py
    @app.errorhandler(ApiException)
    def handle_bad_request(e):
        return_message = {'message': e.message, 'status': e.code}
        if e.result:
            return_message['result'] = e.result
        return jsonify(return_message), e.code

    @app.after_request
    def apply_caching(response):
        # 올바르지 않는 주소입력으로 인해 response.json에 아무것도 담겨있지 않을 경우
        if not response.json:
            return Response(
                    json.dumps({"message": PAGE_NOT_FOUND}),
                    status=404, 
                    mimetype="application/json"
                )

        # error에 잡혀 message에 에러메세지가 이미 담겨있을 경우 그대로 반환
        if 'message' in response.json:
            return Response(
                    json.dumps({"message": response.json['message']}),
                    status=response.json['status'], 
                    mimetype="application/json"
                )

        response = app.response_class(
            response=json.dumps({
                'result': response.json, 
                'message': OK
            }),
            mimetype='application/json'
        )
        return response

    return app

