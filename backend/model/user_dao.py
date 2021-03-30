import pymysql

class UserDao:
    def __init__(self):
        pass

    def find_user_info(self, user_info, connection):
        """ 유저 조회
        Args:
            user_info: 유저정보 dict
            connection: 커넥션

        Returns:
            found_user_info: 유저 username
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            find_user_info_query = """
            SELECT
                username 
            FROM
                user_info
            WHERE
                username = %(username)s
            """

            cursor.execute(find_user_info_query, user_info)
            found_user_info = cursor.fetchone()
        return found_user_info

    def user_identifier(self, user_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            user_identifier_query = """
                SELECT
                    user_type_id, is_delete
                FROM 
                    user_info
                WHERE
                    id = %(user_id)s
            """
            cursor.execute(user_identifier_query, user_info)
            identified_user = cursor.fetchone()
        return identified_user