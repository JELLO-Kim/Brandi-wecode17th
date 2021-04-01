import pymysql


class UserDao:
    def find_user_info(self, user_info, connection):
        """ 유저 조회
        Args:
            user_info: 유저정보 dict
            connection: 커넥션

        Returns:
            found_user_info: 유저 username
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                username 
            FROM
                user_info
            WHERE
                username = %(username)s
            """

            cursor.execute(query, user_info)
            found_user_info = cursor.fetchone()
        return found_user_info

    def user_identifier(self, user_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    user_type_id, is_delete
                FROM 
                    user_info
                WHERE
                    id = %(user_id)s
            """
            cursor.execute(query, user_info)
            identified_user = cursor.fetchone()
        return identified_user

    def create_user_info(self, user_info, connection):
        """ 유저 생성
        Args:
            user_info: 유저정보 dict
            connection: 커넥션
        Returns:
            new_user_info: 생성한 유저의 id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO user_info(
                user_type_id,
                username,
                password,
                phone_number
            )
            VALUES(
                %(user_type_id)s,
                %(username)s,
                %(password)s,
                %(phone_number)s
            )
            """
            cursor.execute(query, user_info)
            new_user_info = cursor.lastrowid
            return new_user_info

    def create_user_info_log(self, user_info, connection):
        """ 유저 이력 생성
        Args:
            user_info: 유저정보 dict
            connection: 커넥션
        Returns:
            new_user_info_log: 생성한 유저 이력 id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO user_info_logs(
                user_info_id,
                user_type_id,
                username,
                password,
                phone_number,
                changer_id,
                change_date
            )
            VALUES(
                %(user_info_id)s,
                %(user_type_id)s,
                %(username)s,
                %(password)s,
                %(phone_number)s,
                %(changer_id)s,
                NOW()
            )
            """
            cursor.execute(query, user_info)
            new_user_info_log = cursor.lastrowid
            return new_user_info_log

    def find_user_email(self, user_info, connection):
        """ 서비스 유저 이메일 조회
        Args:
            user_info: 유저정보 dict
            connection: 커넥션

        Returns:
            found_user: 유저 이메일 정보

        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT email
                FROM users
                WHERE email = %(email)s
            """

            cursor.execute(query, user_info)
            found_user = cursor.fetchone()

            return found_user

    def create_user(self, user_info, connection):
        """ 서비스 유저 생성
        Args:
            user_info: 유저정보 dict
            connection: 커넥션

        Returns:
            new_user: 생성한 서비스 유저 id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO users(
                user_info_id,
                email,
                full_name,
                created_at,
                updated_at
            )
            VALUES(
                %(user_info_id)s,
                %(email)s,
                %(full_name)s,
                NOW(),
                NOW()
            )
            """

            cursor.execute(query, user_info)
            new_user = cursor.lastrowid
            return new_user

    def create_user_log(self, user_info, connection):
        """ 서비스 유저 이력 생성
        Args:
            user_info: 유저정보 dict
            connection: 커넥션

        Returns:
            new_user_log: 생성한 서비스 유저 이력
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO user_logs(
                user_id,
                email,
                full_name,
                created_at,
                updated_at,
                changer_id,
                change_date
            )
            VALUES(
                %(user_id)s,
                %(email)s,
                %(full_name)s,
                NOW(),
                NOW(),
                %(changer_id)s,
                NOW()
            )
            """

            cursor.execute(query, user_info)
            new_user_log = cursor.lastrowid
            return new_user_log

    def find_user_login_info(self, login_info, connection):
        """ 유저 로그인 정보 조회
        Args:
            login_info: 유저 로그인 정보 dict
            connection: 커넥션
        Returns:
            user_login_info: 유저 로그인 정보
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT id, username, password, is_delete
                FROM user_info
                WHERE username= %(username)s 
            """
            cursor.execute(query, login_info)
            user_login_info = cursor.fetchone()
            return user_login_info
