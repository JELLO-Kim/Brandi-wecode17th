import pymysql


class SellerDao:
    def check_existing_product_name(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    name
                FROM
                    products
                WHERE
                    name = %(product_name)s
                AND
                    seller_id = %(user_id)s
            """
            cursor.execute(query, product_info)
            existing_product_name = cursor.fetchone()
            return existing_product_name

    def create_product(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_logs(
                    product_id,
                    seller_id,
                    product_category_id,
                    name,
                    discount_start,
                    discount_end,
                    discount_rate,
                    price,
                    discountPrice,
                    contents_image,
                    created_at,
                    updated_at,
                    is_selling,
                    code,
                    is_display,
                    is_discount,
                    minimum,
                    maximum
                )
                VALUES(
                    %(user_id)s,
                    %(product_category_id)s,
                    %(product_name)s,
                    %(discount_start)s,
                    %(discount_end)s,
                    %(discount_rate)s,
                    %(price)s,
                    %(discount_price)s,
                    %(product_detail_image)s,
                    NOW(),
                    NOW(),
                    %(is_selling)s,
                    FLOOR(RAND() * 901) + 100,
                    %(is_display)s,
                    %(is_discount)s,
                    %(minimum)s,
                    %(maximum)s,
            """
            cursor.execute(query, product_info)
            new_product_id = cursor.lastrowid
            return new_product_id

    def create_product_log(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_logs(
                    product_id,
                    seller_id,
                    product_category_id,
                    name,
                    discount_start,
                    discount_end,
                    discount_rate,
                    price,
                    discountPrice,
                    contents_image,
                    created_at,
                    updated_at,
                    is_selling,
                    code,
                    is_display,
                    is_discount,
                    minimum,
                    maximum,
                    is_delete,
                    changer_id,
                    change_date
                )
                VALUES(
                    %(product_id)s,
                    %(user_id)s,
                    %(product_category_id)s,
                    %(product_name)s,
                    %(discount_start)s,
                    %(discount_end)s,
                    %(discount_rate)s,
                    %(price)s,
                    %(discount_price)s,
                    %(product_detail_image)s,
                    NOW(),
                    NOW(),
                    %(is_selling)s,
                    FLOOR(RAND() * 901) + 100,
                    %(is_display)s,
                    %(is_discount)s,
                    %(minimum)s,
                    %(maximum)s,
                    0,
                    %(user_id)s,
                    SELECT created_at FROM products WHERE id = %(new_product_id)s
                )
            """
            cursor.execute(query, product_info)
            new_product_log_id = cursor.lastrowid
            return new_product_log_id

    def create_product_option(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_options(
                    product_color_type_id,
                    product_size_type_id,
                    product_id,
                    stock 
                ) 
                VALUES(
                    %(product_color_id)s,
                    %(product_size_id)s,
                    %(product_id)s,
                    %(stock)s
                )
            """
            cursor.execute(query, product_info)
            new_product_option_id = cursor.lastrowid
            return new_product_option_id

    def create_product_option_log(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_option_logs(
                    product_option_id,
                    product_color_type_id,
                    product_size_type_id,
                    product_id,
                    stock,
                    changer_id,
                    change_date 
                ) 
                VALUES(
                    %(product_option_id)s,
                    %(product_color_id)s,
                    %(product_size_id)s,
                    %(product_id)s,
                    %(stock)s,
                    %(user_id)s,
                    NOW()
                )
            """
            cursor.execute(query, product_info)
            product_option_log_id = cursor.lastrowid
            return product_option_log_id

    def create_product_thumbnail(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_thumbnails(
                    product_id,
                    image_url,
                    ordering
                )
                VALUES(
                    %(product_id)s,
                    %(product_thumbnail_image)s,
                    1
                )
            """
            cursor.execute(query, product_info)
            product_thumbnail_id = cursor.lastrowid
            return product_thumbnail_id

    def create_product_thumbnail_log(self, product_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_thumbnail_logs(
                    product_thumbnail_id,
                    product_id,
                    image_url,
                    ordering,
                    changer_id,
                    change_date
                )
                VALUES(
                    %(product_thumbnail_id)s,
                    %(product_id)s,
                    %(product_thumbnail_image)s,
                    1,
                    %(user_id)s,
                    NOW()
                )
            """
            cursor.execute(query, product_info)
            product_thumbnail_log_id = cursor.lastrowid
            return product_thumbnail_log_id

    def find_seller_username(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            find_seller_info = """
            SELECT
                username 
            FROM
                user_info
            WHERE
                username = %(username)s
            """
            cursor.execute(find_seller_info, seller_info)
            seller_username = cursor.fetchone()
            return seller_username

    def check_seller_korean_brand_name(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            check_korean_brand_name = """
            SELECT
                korean_brand_name
            FROM
                sellers
            WHERE
                korean_brand_name = %(korean_brand_name)s
            """

            cursor.execute(check_korean_brand_name, seller_info)
            seller_korean_brand_name = cursor.fetchone()
            return seller_korean_brand_name

    def check_seller_english_brand_name(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            check_korean_brand_name = """
            SELECT
                english_brand_name
            FROM
                sellers
            WHERE
                english_brand_name = %(english_brand_name)s
            """

            cursor.execute(check_korean_brand_name, seller_info)
            seller_english_brand_name = cursor.fetchone()
            return seller_english_brand_name

    def create_seller(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            create_seller = """
            INSERT INTO sellers(
                user_info_id,
                seller_category_id,
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
                delivery_information,
                refund_information,
                is_delete
            )
            VALUES(
                %(user_info_id)s,
                %(seller_category_id)s,
                %(korean_brand_name)s,
                %(english_brand_name)s,
                %(customer_service_name)s,
                %(customer_service_opening)s,
                %(customer_service_closing)s,      
                %(customer_service_number)s,
                NOW(),
                NOW(),
                %(image_url)s,
                %(background_image_url)s,
                %(introduce)s,
                %(description)s,
                %(postal_code)s,
                %(address)s,
                %(address_detail)s,
                %(delivery_information)s,
                %(refund_information)s,
                0
            )  
            """
            cursor.execute(create_seller, seller_info)
            new_seller_log_id = cursor.lastrowid
            return new_seller_log_id

    def create_seller_log(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO seller_logs(
                seller_id,
                seller_category_id,
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
                delivery_information,
                refund_information,
                is_delete,
                changer_id,
                change_date
            )
            VALUES(
                %(user_info_id)s,
                %(seller_category_id)s,
                %(korean_brand_name)s,
                %(english_brand_name)s,
                %(customer_service_name)s,
                %(customer_service_opening)s,
                %(customer_service_closing)s,      
                %(customer_service_number)s,
                NOW(),
                NOW(),
                %(image_url)s,
                %(background_image_url)s,
                %(introduce)s,
                %(description)s,
                %(postal_code)s,
                %(address)s,
                %(address_detail)s,
                %(delivery_information)s,
                %(refund_information)s,
                0,
                %(user_info_id)s,
                NOW()
            )  
            """
            cursor.execute(query, seller_info)
            new_seller_log_id = cursor.lastrowid
            return new_seller_log_id

    def login_seller(self, seller_login_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT 
                    id,
                    user_type_id,
                    username, 
                    phone_number,
                    password, 
                    is_delete
                FROM 
                    user_info
                WHERE 
                    username = %(username)s 
            """
            cursor.execute(query, seller_login_info)
            seller = cursor.fetchone()
            return seller

    def create_seller_user_info(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO user_info(
                    user_type_id,
                    username,
                    phone_number,
                    password,
                    is_delete
                )
                VALUES(
                    %(user_type_id)s,
                    %(username)s,
                    %(phone_number)s,
                    %(password)s,
                    0
                )
            """
            cursor.execute(query, seller_info)
            new_seller_id = cursor.lastrowid
            return new_seller_id

    def create_seller_user_info_log(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO user_info_logs(
                    user_info_id,
                    user_type_id,
                    username,
                    phone_number,
                    password,
                    changer_id,
                    change_date
                )
                VALUES(
                    %(user_info_id)s,
                    %(user_type_id)s,
                    %(username)s,
                    %(phone_number)s,
                    %(password)s,
                    %(user_info_id)s,
                    NOW()
                )
            """
            cursor.execute(query, seller_info)
            new_seller_log_id = cursor.lastrowid
            return new_seller_log_id

#채현님 코드
    def seller_edit_get_dao(self, user_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            get_info = """
                SELECT
                    u.username,
                    s.korean_brand_name AS brandKoreand,
                    s.english_brand_name AS brandEnglish,
                    s.image_url AS profile,
                    s.background_image_url AS backgroundImage,
                    s.introduce,
                    s.description,
                    s.customer_service_name AS customerServiceName,
                    CAST(s.customer_service_opening AS CHAR) AS customerServiceOpen,
                    CAST(s.customer_service_closing AS CHAR) AS customerServiceClose,
                    s.customer_service_number AS customerServicePhone,
                    s.postal_code AS postal,
                    s.address,
                    s.address_detail AS addressDetail,
                    s.delivery_information AS deliveryInfo,
                    s.refund_information AS refundInfo
                FROM
                    sellers AS s
                INNER JOIN
                    user_info AS u
                    ON
                        s.user_info_id = u.id
                WHERE
                    s.user_info_id = %(user_id)s
            """
            cursor.execute(get_info, {"user_id": user_id})

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
                    m.seller_id = %(user_id)s

            """
            cursor.execute(manager_info, {"user_id": user_id})

            return cursor.fetchall()

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
            cursor.execute(find_info, {"user_id": user_id})
            find = cursor.fetchall()

            return find

    def update_information(self, seller_edit_info, connection):
        """
        주석 추가 (# 필수입력 정보가 모두 작성되있던 상태에서 일부 값들을 수정할 경우(매니저 제외)) RESTFUL
        """
        print('??????????????????????????????????')
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
            if seller_edit_info['postalCode']:
                query += """
                    postal_code = %(postalCode)s,
                """
            if seller_edit_info['address']:
                query += """
                    address = %(address)s,
                """
            if seller_edit_info['detailAddress']:
                query += """
                    address_detail = %(detailAddress)s,
                """
            if seller_edit_info['delivery_info']:
                query += """
                    delivery_info = %(delivery_info)s,
                """
            if seller_edit_info['refund_info']:
                query += """
                    refund_info = %(refund_info)s,
                """
            if seller_edit_info['callName']:
                query += """
                    customer_service_name = %(callName)s,
                """
            if seller_edit_info['callStart']:
                query += """
                    customer_service_opening = %(callStart)s,
                """
            if seller_edit_info['callEnd']:
                query += """
                    customer_service_closing = %(callEnd)s,
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
            return len(changed_value) - 1

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
            cursor.execute(check_manager_query, {"user_id": user_id})

            return cursor.fetchone()

    # 들어온 값 중이 이미 존재하는 값이 있을 경우 에러 반환
    def check_seller_manager(self, seller_edit_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            manager_query = """
                    SELECT
                        m.id,
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
            cursor.execute(manager_query, {"user_id": seller_edit_info['user_id']})
            return cursor.fetchall()

    # 이미 작성된 manager의 정보 수정
    def update_manager(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            edit_manager = """
                UPDATE
                    managers
                SET
            """
            if one['name']:
                edit_manager += """
                    name = %(name)s,
                """
            if one['email']:
                edit_manager += """
                    email = %(email)s,
                """
            if one['phone']:
                edit_manager += """
                    phone_number = %(phone)s,
                """
            edit_manager += """
                updated_at = now()
            """

            cursor.execute(edit_manager, one)
            return cursor.fetchone()

    # 들어온 값에 대한 manager 신규 생성
    def insert_information_manager(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            print('dao에서 받는 one=====', one)
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
            return cursor.lastrowid

    def create__manager_logs(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            log_query = """
                INSERT INTO
                    manager_logs(
                        name,
                        email,
                        phone_number,
                        seller_id
                    )
                SELECT
                    m.name,
                    m.email,
                    m.phone_number,
                    %(user_id)s
                FROM
                    managers AS m
                )

            """

    # seller_logs 생성
    def create_seller_update_log(self, user_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            log_query = """
                INSERT INTO
                    seller_logs(
                        seller_id,
                        seller_tier_type_id,
                        seller_category_id,
                        seller_level_type_id,
                        korean_brand_name,
                        english_brand_name,
                        customer_service_name,
                        customer_serice_opening,
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
                        s.seller_tier_type_id,
                        s.seller_category_id,
                        s.seller_level_type_id,
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
            cursor.execute(log_query, {"user_id": user_id})

            return cursor.fetchone()

