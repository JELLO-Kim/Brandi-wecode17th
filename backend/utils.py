import io, jwt, uuid

from functools import wraps
from flask import request, jsonify, g

from config import SECRET_KEY, ALGORITHM
from db_connector import connect_db
from model.user_dao import UserDao
from exceptions import *


def login_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('AUTHORIZATION')
        try:
            if access_token:
                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                user_id = payload['user_id']
                connection = connect_db()
                user_info = {'user_id': user_id}
                user_dao = UserDao()
                user = user_dao.user_identifier(user_info, connection)

                if not user:
                    raise ApiException(400, INVALID_USER)
                if user['is_delete'] == 1:
                    raise ApiException(400, USER_HAS_BEEN_DELETED)

                g.token_info = {
                    'user_id': user_id,
                    'user_type_id': user['user_type_id'],
                }
                return func(*args, **kwargs)

            else:
                raise ApiException(401, LOGIN_REQUIRED)

        except jwt.InvalidTokenError:
            raise ApiException(400, INVALID_TOKEN)
        except ApiException as e:
            raise e

    return wrapper



