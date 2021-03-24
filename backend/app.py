from flask import Flask, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_migrate import migrate
from decimal import Decimal
from datetime import datetime
from exceptions import *
from view import UserView, OrderView


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
    app.config.from_pyfile('config.py')
    app.register_blueprint(UserView.user_app)
    app.register_blueprint(OrderView.order_app)
    # 모든 곳에서 호출하는 것을 허용
    CORS(app, resources={'*': {'origins': '*'}})

#    @app.after_request
#    def apply_caching(response):
#        response = app.response_class(
#            response=json.dumps({
#                'result': response.json,
#                'message': OK
#            }),
#            mimetype='application/json'
#        )
#        return response

    @app.errorhandler(ApiException)
    def handle_error(e):
        return_message = {'message': e.message}
        if e.extra is not None:
            return_message['result'] = e.extra
        return jsonify(return_message), e.code

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    return app
