from model.user_dao import UserDao
from flask import jsonify
import bcrypt
import jwt
from responses import *
from config import SECRET_KEY, ALGORITHM


class UserService:
    def __init__(self):
        pass

    def create_user(self, user_info, connection):
        """ 유저 회원가입
        Author: Mark Hasung Kim
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
            created_user: 새로 회원가입한 유저 id
        """
        user_dao = UserDao()
        username_exists = user_dao.find_user_info(user_info, connection)
        if username_exists:
            raise ApiException(400, DUPLICATED_USERNAME)

        hashed_password = bcrypt.hashpw(
            user_info['password'].encode('utf-8'), bcrypt.gensalt())
        user_info['password'] = hashed_password
        user_info_id = user_dao.create_user_info(user_info, connection)
        user_info['user_info_id'] = user_info_id
        user_dao.create_user_info_log(user_info, connection)
        email_exists = user_dao.find_user_email(user_info, connection)

        if email_exists:
            raise ApiException(400, DUPLICATED_EMAIL)

        user_info['full_name'] = '' #TODO: user_signup does not require full_name

        created_user = user_dao.create_user(user_info, connection)
        user_dao.create_user_log(user_info, connection)

        return created_user

    def signin_user(self, login_info, connection):
        """ 유저 로그인
        Author: Mark Hasung Kim
        Args:
            login_info (dict): 유저 로그인 정보
            connection: 커넥션
        Returns:
             jsonify({'accessToken': token, 'userId': user_id}), 201
             (유저 토큰이랑 user_id 반환해준다)
        """
        user_dao = UserDao()
        user = user_dao.find_user_login_info(login_info, connection)

        if user['user_type_id'] != 1:
            raise ApiException(403, IS_NOT_SERVICE_USER)

        if user:
            if bcrypt.checkpw(login_info['password'].encode('utf-8'), user['password'].encode('utf-8')):
                token = jwt.encode(
                    {'user_id': user['id']}, SECRET_KEY, ALGORITHM)
                user_id = user['id']
                return jsonify({'accessToken': token, 'userId': user_id}), 201
            if user['is_delete'] == 1:
                raise ApiException(400, USER_NOT_FOUND)
            raise ApiException(400, PASSWORD_MISMATCH)
        raise ApiException(400, USER_NOT_FOUND)
