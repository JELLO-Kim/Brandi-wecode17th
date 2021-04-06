import pymysql

class SellerDao:
    def check_existing_product_name(self, product_info, connection):
        """ [어드민] 셀러의 등록된 상품중에 이미 존재하는 상품 명을 또 추가할때 조회
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품에대한 정보
            connection: 커넥션
        Returns:
            existing_product_name (존재하는 상품 명)
        """
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
        """ [어드민] 셀러 상품 생성
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품애대한 정보
            connection: 커넥션
        Returns:
            new_product_id (새로 생성된 상품 id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO products(
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
                    is_delete
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
                    0
                )
            """
            cursor.execute(query, product_info)
            new_product_id = cursor.lastrowid
            return new_product_id

    def update_product(self, product_info, connection):
        """ [어드민] 셀러 상품 수정
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 수정 하고싶은 상품애대한 정보
            connection: 커넥션
        Returns:
            updated_product_id (수정된 상품 id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    products
                SET
            """
            if product_info.get('is_selling'):
                query += """
                    is_selling = %(is_selling)s,
                """
            if product_info.get('is_display'):
                query += """
                    is_display = %(is_display)s,
                """
            if product_info.get('product_category_id'):
                query += """
                    product_category_id = %(product_category_id)s,
                """
            if product_info.get('product_name'):
                query += """
                    name = %(product_name)s,
                """
            if product_info.get('product_detail_image'):
                query += """
                    contents_image = %(product_detail_image)s,
                """
            if product_info.get('price'):
                query += """
                    price = %(price)s,
                """
            if product_info.get('minimum'):
                query += """
                    minimum = %(minimum)s,
                """
            if product_info.get('maximum'):
                query += """
                    maximum = %(maximum)s,
                """
            if product_info.get('discount_rate'):
                query += """
                    discount_rate = %(discount_rate)s,
                """
            if product_info.get('discount_price'):
                query += """
                    discountPrice = %(discount_price)s,
                """
            if product_info.get('discount_start'):
                query += """
                    discount_start = %(discount_start)s,
                """
            if product_info.get('discount_end'):
                query += """
                    discount_end = %(discount_end)s,
                """
            if product_info.get('is_discount'):
                query += """
                    is_discount = %(is_discount)s,
                """
            query += """
                    updated_at = NOW()
                WHERE
                    id = %(product_id)s
            """
            cursor.execute(query, product_info)
            updated_product_id = cursor.lastrowid
            return updated_product_id

    def soft_delete_product(self, product_info, connection):
        """ [어드민] 상품 soft delete (is_delete = 1)
        Author: Mark Hasung Kim
        Args:
            product_info: product_id를 갖고있는 dict
            connection: 커넥션
        Returns:
            deleted_product_id (삭제된 product_id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    products
                SET
                    is_delete = 1,
                    updated_at = NOW()
                WHERE
                    id = %(product_id)s
            """
            cursor.execute(query, product_info)
            deleted_product_id = cursor.lastrowid
            return deleted_product_id

    def create_product_log(self, product_info, connection):
        """ [어드민] product_log 생성
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품에대한 정보
            connection: 커넥션
        Returns:
            new_product_log_id (생성된 product_log id)
        """
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
                SELECT
                    p.id,
                    p.seller_id,
                    p.product_category_id,
                    p.name,
                    p.discount_start,
                    p.discount_end,
                    p.discount_rate,
                    p.price,
                    p.discountPrice,
                    p.contents_image,
                    p.created_at,
                    p.updated_at,
                    p.is_selling,
                    p.code,
                    p.is_display,
                    p.is_discount,
                    p.minimum,
                    p.maximum,
                    p.is_delete,
                    %(user_id)s,
                    p.updated_at
                FROM
                    products AS p
                WHERE
                    p.id = %(product_id)s
            """
            cursor.execute(query, product_info)
            new_product_log_id = cursor.lastrowid
            return new_product_log_id

    def create_product_option(self, product_info, connection):
        """ [어드민] product_option 생성
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품에대한 정보
            connection: 커넥션
        Returns:
            new_product_option_id (생성된 product_option id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_options(
                    product_color_type_id,
                    product_size_type_id,
                    product_id,
                    stock,
                    created_at,
                    updated_at
                ) 
                VALUES(
                    %(product_color_id)s,
                    %(product_size_id)s,
                    %(product_id)s,
                    %(stock)s,
                    NOW(),
                    NOW()
                )
            """
            cursor.execute(query, product_info)
            new_product_option_id = cursor.lastrowid
            return new_product_option_id

    def soft_delete_product_option(self, product_info, connection):
        """ [어드민] product_option soft delete
        Author: Mark Hasung Kim
        Args:
            product_info: product_option_id를 갖고있는 dict
            connection: 커넥션
        Returns:
            deleted_product_option (삭제된 product_option_id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    product_option_logs
                SET
                    is_delete = 1,
                    updated_at = NOW()
                WHERE
                    id = %(product_option_id)s    
            """
            cursor.execute(query, product_info)
            deleted_product_option = cursor.lastrowid
            return deleted_product_option

    def create_product_option_log(self, product_info, connection):
        """ [어드민] product_option_log 생성
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품에대한 정보
            connection: 커넥션
        Returns:
            product_option_log_id (생성된 product_option_log id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_option_logs(
                    product_option_id,
                    product_color_type_id,
                    product_size_type_id,
                    product_id,
                    stock,
                    changer_id,
                    change_date,
                    created_at,
                    updated_at 
                )
                SELECT
                    po.id,
                    po.product_color_type_id,
                    po.product_size_type_id,
                    po.product_id,
                    po.stock,
                    %(user_id)s,
                    po.updated_at,
                    po.created_at,
                    po.updated_at
                FROM
                    product_options AS po
                WHERE
                    po.id = %(product_option_id)s
            """
            cursor.execute(query, product_info)
            product_option_log_id = cursor.lastrowid
            return product_option_log_id

    def create_new_product_thumbnail(self, product_info, connection):
        """ [어드민] product_thumbnail image 생성
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품에대한 정보
            connection: 커넥션
        Returns:
            product_thumbnail_id (생성된 product_thumbnail id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_thumbnails(
                    product_id,
                    image_url,
                    is_delete,
                    ordering
                )
                SELECT
                    %(product_id)s,
                    %(image_url)s,
                    0,
                    IFNULL(MAX(pt.ordering), 0) + 1
                FROM
                    product_thumbnails AS pt
                WHERE
                    pt.product_id = %(product_id)s
                    AND
                    pt.is_delete = 0
            """
            cursor.execute(query, product_info)
            product_thumbnail_id = cursor.lastrowid
            return product_thumbnail_id

    def delete_product_thumbnail(self, product_info, connection):
        """ [어드민] product_thumbnail image 삭제
        Author:
            Mark Hasung Kim
        Args:
            product_info: 셀러가 삭제 하고싶은 상품 이비지 정보
            connection: 커넥션
        Returns:
            product_thumbnail_id (생성된 product_thumbnail id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    product_thumbnails
                SET
                    is_delete = 1
                WHERE
                    id = %(product_thumbnail_id)s
            """
            cursor.execute(query, product_info)
            deleted_product_thumbnail_id = cursor.lastrowid
            return deleted_product_thumbnail_id

    def create_product_thumbnail_log(self, product_info, connection):
        """ [어디민] product_thumbnail_log 생성
        Author: Mark Hasung Kim
        Args:
            product_info: 셀러가 등록 하고싶은 상품에대한 정보
            connection: 커넥션
        Returns:
            product_thumbnail_log_id (생성된 product_thumbnail_log id)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO product_thumbnail_logs(
                    product_thumbnail_id,
                    product_id,
                    image_url,
                    ordering,
                    changer_id,
                    change_date,
                    is_delete
                )
                SELECT
                    pt.id,
                    pt.product_id,
                    pt.image_url,
                    pt.ordering,
                    %(user_id)s,
                    NOW(),
                    pt.is_delete
                FROM
                    product_thumbnails AS pt
                WHERE
                    pt.id = %(product_thumbnail_id)s 
            """
            cursor.execute(query, product_info)
            product_thumbnail_log_id = cursor.lastrowid
            return product_thumbnail_log_id

    def get_all_product_categories(self, connection):
        """ [어드민] 모든 상품 카테고리 갖고오기
        Author: Mark Hasung Kim
        Args:
            connection: 커넥션
        Returns:
            product_categories (모든 상품 카테고리를 dict형식으로 반환해준다)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id,
                    parent_id,
                    name,
                    level,
                    is_delete
                FROM
                    product_categories
            """
            cursor.execute(query)
            product_categories = cursor.fetchall()
            return product_categories

    def get_all_product_colors(self, connection):
        """ [어드민] 모든 상품 색갈 갖고오기
        Author: Mark Hasung Kim
        Args:
            connection: 커넥션
        Returns:
            product_color_types (모든 상품 색갈들을 dict형식으로 반환해준다)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id,
                    name,
                    ordering,
                    is_delete
                FROM
                    product_color_types
            """
            cursor.execute(query)
            product_color_types = cursor.fetchall()
            return product_color_types

    def get_all_product_sizes(self, connection):
        """ [어드민] 모든 상품 사이즈 갖고오기
        Author: Mark Hasung Kim
        Args:
            connection: 커넥션
        Returns:
            product_size_types (모든 상품 사이즈들을 dict형식으로 반환해준다)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id,
                    name,
                    ordering,
                    is_delete 
                FROM
                    product_size_types
            """
            cursor.execute(query)
            product_size_types = cursor.fetchall()
            return product_size_types

    def get_product_colors_sizes(self, product_info, connection):
        """ [어드민] 상품의 모든 커러id, 사이즈id, stock 갖고오기
        Author:
            Mark Hasung Kim
        Args:
            product_info: product_id를 가지고있는 dict
            connection: 커넥션
        Returns:
            product_colors_sizes (dict형식으로 커러id, 사이즈id, stock을 반환해준다)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    product_color_type_id,
                    product_size_type_id,
                    stock
                FROM
                    product_options
                WHERE
                    product_id = %(product_id)s
                    AND
                    is_delete = 0
            """
            cursor.execute(query, product_info)
            product_colors_sizes = cursor.fetchall()
            return product_colors_sizes

    def get_product_details(self, product_info, connection):
        """ [어드민] 상품 상세 정보 갖고오기
        Author:
            Mark Hasung Kim
        Args:
            product_info: product_id를 가지고있는 dict
            connection: 커넥션
        Returns:
            product_details (dict형식으로 상품 상세정보를 반환해준다)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    name,
                    price,
                    product_category_id,
                    discount_start,
                    discount_end,
                    discount_rate,
                    discountPrice,
                    contents_image,
                    is_selling,
                    is_display,
                    minimum,
                    maximum
                FROM
                    products
                WHERE
                    id = %(product_id)s
            """
            cursor.execute(query, product_info)
            product_details = cursor.fetchone()
            return product_details

    def get_product_thumbnails(self, product_info, connection):
        """ [어드민] 상품 thumbnail사진 url, id 갖고오기
        Author:
            Mark Hasung Kim
        Args:
            product_info: product_id를 가지고있는 dict
            connection: 커넥션
        Returns:
            product_thumbnails (dict형식으로 상품의 모든 thumbnail사진 정보를 반환해준다)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id,
                    image_url
                FROM
                    product_thumbnails
                WHERE
                    product_id = %(product_id)s
                    AND
                    is_delete = 0
            """
            cursor.execute(query, product_info)
            product_thumbnails = cursor.fetchall()
            return product_thumbnails

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
                customer_service_number,
                created_at,
                updated_at,
                is_delete
            )
            VALUES(
                %(user_info_id)s,
                %(seller_category_id)s,
                %(korean_brand_name)s,
                %(english_brand_name)s,     
                %(customer_service_number)s,
                NOW(),
                NOW(),
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
            SELECT
                s.user_info_id,
                s.seller_category_id,
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
                s.delivery_information,
                s.refund_information,
                s.is_delete,
                %(user_info_id)s,
                s.updated_at
            FROM
                sellers AS s
            WHERE
                s.user_info_id = %(user_info_id)s
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
                    password
                )
                VALUES(
                    %(user_type_id)s,
                    %(username)s,
                    %(phone_number)s,
                    %(password)s
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
                SELECT
                    ui.id,
                    ui.user_type_id,
                    ui.username,
                    ui.phone_number,
                    ui.password,
                    ui.id,
                    NOW()
                FROM
                    user_info AS ui
                WHERE
                    ui.id = %(user_info_id)s
            """
            cursor.execute(query, seller_info)
            new_seller_log_id = cursor.lastrowid

    # 채현 : 정보수정페이지 내용 가져오기 (get)
    def seller_edit_get_dao(self, user, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            get_info = """
                SELECT
                    u.username,
                    s.korean_brand_name AS brandKorean,
                    s.english_brand_name AS brandEnglish,
                    s.image_url AS profile,
                    sl.name AS sellerStatus,
                    sc.name AS sellerCategory,
                    sc.id AS sellerCategoryId,
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
                INNER JOIN user_info AS u
                    ON s.user_info_id = u.id
                INNER JOIN seller_level_types AS sl
                    ON s.seller_level_type_id  = sl.id
                INNER JOIN seller_categories AS sc
                    ON s.seller_category_id = sc.id
                WHERE
                    s.user_info_id = %(user_id)s
            """
            cursor.execute(get_info, {"user_id": user['user_id']})

            return cursor.fetchone()
    # 채현 : seller의 manager 정보 가져오기
    def get_seller_manager(self, user, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            manager_info = """
                SELECT
                    m.id,
                    m.name,
                    m.email,
                    m.phone_number AS phoneNumber
                FROM
                    managers AS m
                WHERE
                    m.seller_id = %(user_id)s
                    AND
                    is_delete = 0
                ORDER BY
                    m.ordering ASC
            """
            cursor.execute(manager_info, {"user_id": user['user_id']})

            return cursor.fetchall()
    # 채현 : seller의 정보수정내용 중 필수입력란만 확인하기
    # 수정화면을 처음 들어갔는지 확인하는 쿼리문(처음이라면 모든 값이 null)
    def find_seller_info(self, user, connection):
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
            cursor.execute(find_info, {"user_id": user['user_id']})

            return cursor.fetchone()
    # 채현 : 들어온 값들에 대해 update 해주기 (patch)
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
                    delivery_information = %(delivery_info)s,
                """
            if seller_edit_info['refund_info']:
                query += """
                    refund_information = %(refund_info)s,
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
            if seller_edit_info['brandKorean']:
                query += """
                    korean_brand_name = %(brandKorean)s,
                """
            if seller_edit_info['brandEnglish']:
                query += """
                    english_brand_name = %(brandEnglish)s,
                """
            query += """
                    updated_at = now()
                WHERE
                    user_info_id = %(user_id)s
            """

            cursor.execute(query, seller_edit_info)
            return cursor.lastrowid

    # 수정되는 유저에 배당된 is_delete=0 인 매니저의 수 파악
    def check_seller_manager_number(self, user, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            check_manager_number = """
                SELECT
                    COUNT(*) AS totalCount
                FROM
                    managers AS m
                WHERE
                    m.seller_id = %(user_id)s
                    AND
                    m.is_delete = 0
            """
            cursor.execute(check_manager_number, {"user_id": user['user_id']})

            return cursor.fetchone()

    # 이미 작성된 manager의 정보 수정
    def update_manager(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            edit_manager = """
                UPDATE
                    managers
                SET
                    name = %(name)s,
                    email = %(email)s,
                    phone_number = %(phoneNumber)s,
                    updated_at = now()
                WHERE
                    id = %(id)s
            """
            cursor.execute(edit_manager, one)
            return True

    # 들어온 값에 대한 manager 신규 생성
    def insert_information_manager(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            manager_query = """
                INSERT INTO
                        managers
                        (
                            seller_id,
                            name,
                            email,
                            phone_number,
                            ordering
                        )
                        VALUES
                        (
                            %(user_id)s,
                            %(name)s,
                            %(email)s,
                            %(phoneNumber)s,
                            (
                                SELECT
                                    IFNULL(MAX(om.ordering), 0)+1
                                FROM
                                    managers AS om
                                WHERE
                                    om.seller_id = %(user_id)s
                            )
                        )
            """
            cursor.execute(manager_query, one)
            return cursor.lastrowid

    # soft_delete 결과 is_delete의 값을 1로 바꾸어 주는 로직
    def delete_manager_dao(self, extra, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            delete_query = """
                UPDATE
                    managers
                SET
                    is_delete = 1
                WHERE
                    id = %(change_id)s
            """
            cursor.execute(delete_query, {"change_id" : extra['manager_id']})
            return True

    # manager 이력 생성
    def create_manager_log(self, one, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            log_query = """
                INSERT INTO
                    manager_logs(
                        manager_id,
                        name,
                        email,
                        phone_number,
                        created_at,
                        updated_at,
                        seller_id,
                        changer_id,
                        change_date,
                        is_delete
                    )
                SELECT
                    m.id,
                    m.name,
                    m.email,
                    m.phone_number,
                    m.created_at,
                    m.updated_at,
                    m.seller_id,
                    %(changer_id)s,
                    now(),
                    m.is_delete
                FROM
                    managers AS m
                WHERE
                    m.id = %(change_id)s
            """
            cursor.execute(log_query, {"change_id" : one['id'], 'changer_id' : one['changer_id']})
            return True

    # seller 이력 생성
    def create_seller_update_log(self, user, connection):
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
                        %(changer_id)s,
                        now()
                    FROM
                        sellers AS s
                    WHERE
                        s.user_info_id = %(user_id)s
                """
            cursor.execute(log_query, {"user_id" : user['user_id'], "changer_id": user['changer_id']})

            return True
