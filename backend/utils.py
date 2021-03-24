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
        access_token = request.headers.get('AUTHORIZATION', None)

        if access_token:
            try:
                payload    = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                user_id    = payload['user_id']
                connection = connect_db()
                user_dao   = UserDao()
                user       = user_dao.user_identifier(user_info, connection)
                if not user:
                    raise (400, USER_DOES_NOT_EXIST)
                if user['is_delete'] == 1:
                    raise(400, USER_DOES_NOT_EXIST)
                g.token_info = {
                    'user_id': user_id,
                    'user_type_id': user['user_type_id'],
                }
                return func(*args, **kwargs)

            except Exception as e:
                raise (500, INTERNAL_SERVER_ERROR)
            except jwt.InvalidTokenError:
                raise (401, INVALID_USER)
            except not connection:
                raise (500, INTERNAL_SERVER_ERROR)
    return wrapper



