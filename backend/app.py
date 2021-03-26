import json

from flask  import Flask, jsonify, Response
from view   import ProductView
from errors import *
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ProductView.product_app)
    CORS(app, resources={'*': {'origins': '*'}})
    
    @app.after_request
    def apply_caching(response):
        # 올바르지 않는 주소입력으로 인해 response.json에 아무것도 담겨있지 않을 경우
        if not response.json :
            return Response(
                    json.dumps({"message" : PAGE_NOT_FOUND}), 
                    status=404, 
                    mimetype="application/json"
                )

        # error에 잡혀 message에 에러메세지가 이미 담겨있을 경우 그대로 반환
        if 'message' in response.json:
            return Response(
                    json.dumps({"message" : response.json['message']}), 
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

    # error 메세지 반환 from errors.py
    @app.errorhandler(ApiException)
    def handle_bad_request(e):
        return_message = {}
        return_message['message'] = e.message
        return_message['status'] = e.code
        if e.result:
            return_message['result'] = e.result
        return jsonify(return_message), e.code

    return app
