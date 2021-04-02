import pymysql


class SellerDao:
    def create_product(self, product_info, connection):
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
                    %(maximum)s
                )
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
                INSERT INTO product_options(
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
                    %(new_product_id)s,
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
                INSERT INTO product_thumbnails(
                    product_thumbnail_id,
                    product_id,
                    image_url,
                    ordering,
                    changer_id,
                    change_date
                )
                VALUES(
                    %(product_thumbnail_id)s,
                    %(new_product_id)s,
                    %(product_thumbnail_image)s,
                    1,
                    %(user_id)s,
                    NOW()
                )
            """
            cursor.execute(query, product_info)
            product_thumbnail_log_id = cursor.lastrowid
            return product_thumbnail_log_id
