import pymysql

class SellerDao:
    # 확인!!! : 매니저 id / 이름 / 이메일 / 폰번호
    def seller_edit_get_dao(self, user_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            get_info = """
                SELECT
                    u.username,
                    s.korean_brand_name,
                    s.english_brand_name,
                    s.image_url,
                    s.background_image_url,
                    s.introduce,
                    s.description,
                    s.customer_service_name,
                    s.customer_service_opening,
                    s.customer_service_closing,
                    s.customer_service_number,
                    s.postal_code,
                    s.address,
                    s.address_detail,
                    s.delivery_information,
                    s.refund_information
                FROM
                    sellers AS s
                INNER JOIN
                    user_info AS u
                    ON
                        s.user_info_id = u.id
                WHERE
                    s.user_info_id = %(user_id)s
            """
            cursor.execute(get_info, {"user_id" : user_id})

            return cursor.fetchone()

    def get_seller_manager(self, user_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            manager_info = """
                SELECT
                    m.id,
                    m.name,
                    m.email,
                    m.phone_number
                FROM
                    managers AS m
                WHERE
                    m.seller_id = 6
            """
            cursor.execute(manager_info, {"user_id" : user_id})
            
            return cursor.fetchall()


        """ 이전에 서브쿼리로 작성한 manager 정보 SQL문
                            (
                                SELECT
                                    m.name
                                FROM 
                                    brandi.managers AS m
                                WHERE
                                    m.seller_id = %(user_id)s
                                AND
                                    m.ordering = 1
                            ) AS manager_name,
                            (
                                SELECT
                                    m.phone_number
                                FROM 
                                    brandi.managers AS m
                                WHERE
                                    m.seller_id = %(user_id)s
                                AND
                                    m.ordering = 1
                            ) AS manager_phone,
                            (
                                SELECT
                                    m.email
                                FROM 
                                    brandi.managers AS m
                                WHERE
                                    m.seller_id = %(user_id)s
                                AND
                                    m.ordering = 1
                            ) AS manager_email
        """

    # 수정화면을 처음 들어갔는지 확인하는 쿼리문(처음이라면 모든 값이 null)
    def find_seller_info(self, user_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            find_info = """
                SELECT
                    s.image_url,
                    s.introduce,
                    s.customer_service_opening,
                    s.customer_service_closing,
                    s.address,
                    s.delivery_information,
                    s.refund_information
                FROM
                    sellers AS s
                LEFT JOIN
                    managers AS m
                ON
                    m.seller_id = s.user_info_id
                WHERE
                    s.user_info_id = %(user_id)s
            """
            cursor.execute(find_info, {"user_id" : user_id})
            find = cursor.fetchall()

            return find

    def update_information(self, seller_edit_info, connection):
        """
        주석 추가 (# 필수입력 정보가 모두 작성되있던 상태에서 일부 값들을 수정할 경우(매니저 제외)) RESTFUL
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    sellers
                SET
            """
            if seller_edit_info['profile']:
                query += """
                    image_url = %(profile)s,
                """
            if seller_edit_info['introduce']:
                query += """
                    introduce = %(introduce)s,
                """
            if seller_edit_info['description']:
                query += """
                    description = %(description)s,
                """
            if seller_edit_info['postal_code']:
                query += """
                    postal_code = %(postal)s,
                """
            if seller_edit_info['address']:
                query += """
                    address = %(address)s,
                """
            if seller_edit_info['detail_address']:
                query += """
                    address_detail = %(detail_address)s,
                """
            if seller_edit_info['delivery_info']:
                query += """
                    delivery_info = %(delivery_info)s,
                """
            if seller_edit_info['refund_info']:
                query += """
                    refund_info = %(refund_info)s,
                """
            if seller_edit_info['call_name']:
                query += """
                    customer_service_name = %(call_name)s,
                """
            if seller_edit_info['call_start']:
                query += """
                    customer_service_opening = %(call_start)s,
                """
            if seller_edit_info['call_end']:
                query += """
                    customer_service_closing = %(call_end)s,
                """
            query += """
                    updated_at = now()
                WHERE
                    user_info_id = %(user_id)s
            """

            cursor.execute(query, seller_edit_info)

            # 새로 변경된 값이 담긴 배열 생성 (token으로 부터 받은 user_id도 포함됨)
            values = [a for a in seller_edit_info.values()]
            changed_value = []
            for row in values:
                if row is not None:
                    changed_value.append(row)
                    
            # 실제로 새로 입력받은 seller의 정보갯수 반환
            return len(changed_value)-1

    # 수정되는 유저에 배당된 is_delete=0 인 매니저의 수 파악
    def check_seller_manager(self, user_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            check_manager_query = """
                SELECT
                    COUNT(*)
                FROM
                    managers AS m
                WHERE
                    m.user_info_id = %(user_id)s
                    AND
                    m.is_delete=0
            """
            cursor.execute(check_manager_query, {"user_id" : user_id})

            return cursor.fetchone()

    # 들어온 값 중이 이미 존재하는 값이 있을 경우 에러 반환
    def check_seller_manager(self, seller_edit_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            manager_query = """
                    SELECT
                        m.name,
                        m.email,
                        m.phone_number
                    FROM
                        managers AS m
                    WHERE
                        m.seller_id = %(user_id)s
                        AND
                        is_delete = 0
                """
            cursor.execute(manager_query, {"user_id" : seller_edit_info['user_id']})
            return cursor.fetchall()

    # 들어온 값에 대한 manager 생성
    def update_information_manager(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            manager_query = """
                    INSERT INTO
                        managers
                        (
                            seller_id,
                            name,
                            email,
                            phone_number
                        )
                    VALUES
                    (
                        %(user_id)s,
                        %(name)s,
                        %(email)s,
                        %(phone)s
                    )
                """
            cursor.execute(manager_query, one)
            return cursor.fetchall()


    # log 테이블 생성
    def create_seller_update_log(self, seller_edit_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            log_query = """
                INSERT INTO
                    seller_log(
                        seller_id,
                        seller_tier_type_id,
                        seller_category_id,
                        seller_statistics_id,
                        seller_action_level_type_id,
                        korean_brand_name,
                        english_brand_name,
                        customer_service_name,
                        customer_service_opening,
                        customer_service_closing,
                        customer_service_number,
                        created_at,
                        updated_at,
                        image_url,
                        background_image_url,
                        introduce,
                        description,
                        postal_code,
                        address,
                        address_detail,
                        is_weekend,
                        delivery_information,
                        refund_information,
                        is_delete,
                        changer_id,
                        change_date
                    )
                    SELECT
                        s.user_info_id,
                        s.seller_tire_type_id,
                        s.seller_category_id,
                        s.seller_statistics_id,
                        s.seller_action_level_type_id,
                        s.korean_brand_name,
                        s.english_brand_name,
                        s.customer_service_name,
                        s.customer_service_opening,
                        s.customer_service_closing,
                        s.customer_service_number,
                        s.created_at,
                        s.updated_at,
                        s.image_url,
                        s.background_image_url,
                        s.introduce,
                        s.description,
                        s.postal_code,
                        s.address,
                        s.address_detail,
                        s.is_weekend,
                        s.delivery_information,
                        s.refund_information,
                        s.is_delete,
                        %(user_id)s,
                        now()
                    FROM
                        sellers AS s
                    WHERE
                        s.user_info_id = %(user_id)s
                """
            cursor.execute(log_query, {"user_id" : user_id})

            return cursor.fetchone()