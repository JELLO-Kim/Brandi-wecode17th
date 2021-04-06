from flask import request, Blueprint, jsonify
from service.user_service import UserService
from db_connector import connect_db
from responses import *
from validators import validate_email, validate_password


class UserView:
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    @user_app.route('signup', methods=['POST'])
    def sign_up_user():
        """ 유저 회원가입
        Author: Mark Hasung Kim
        Returns:
            {
                "custom_message": "SERVICE_USER_CREATED,
                "result": "POST
                }
        """
        connection = None
        try:
            data = request.json
            if 'username' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'email' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'password' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'user_type_id' not in data:
                raise ApiException(400, INVALID_INPUT)

            if not validate_password(data['password']):
                raise ApiException(400, INVALID_PASSWORD)
            if not validate_email(data['email']):
                raise ApiException(400, INVALID_EMAIL)

            user_info = {
                'username': data['username'],
                'email': data['email'],
                'password': data['password'],
                'user_type_id': int(data['user_type_id']),
                'phone_number': '',
            }

            connection = connect_db()
            user_service = UserService()
            user_service.create_user(user_info, connection)
            connection.commit()

            return {"custom_message": "SERVICE_USER_CREATED", "result": "POST"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @user_app.route('signin', methods=['POST'])
    def signin_user():
        """ 유저 로그인
        Author: Mark Hasung Kim
        Returns:
             user_info: 유저 로그인 토큰
        """
        connection = None
        try:
            data = request.json

            if 'username' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'password' not in data:
                raise ApiException(400, INVALID_INPUT)

            login_info = {
                'username': data['username'],
                'password': data['password']
            }

            connection = connect_db()
            user_service = UserService()
            user_info = user_service.signin_user(login_info, connection)
            return user_info

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
