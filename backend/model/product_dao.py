from flask  import jsonify
from errors import *

import pymysql

class ProductDao:

    # category 정보
    def products_category(self, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            category_info = """
                SELECT
                    c.id,
                    c.name,
                    c.parent_id
                FROM
                    product_categories AS c
                """

            cursor.execute(category_info)
            categories=cursor.fetchall()

        return categories

    #products 정보
    def products_list(self, filter_data, connection, page_condition):
        self.page_condition = page_condition
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            products_info = """
                SELECT
                    p.id,
                    s.korean_brand_name AS sellerName,
                    name,
                    CAST(ROUND(discount_rate, 0) AS CHAR) AS discountRate,
                    CAST(ROUND(p.price, -2) AS CHAR) AS price,
                    CAST(p.discounted_price AS CHAR) AS discountPrice,
                    min(i.image_url) AS thumbnailImage,
                    p.total_sales AS totalSales
                FROM
                    products AS p
                INNER JOIN
                    sellers AS s
                ON
                    p.seller_id=s.user_info_id
                INNER JOIN
                    user_info AS u
                ON
                    s.user_info_id=u.id
                LEFT JOIN
                    product_thumbnails AS i
                ON
                    p.id=i.product_id
                WHERE
                    p.is_selling=1
                """

            if 'category' in filter_data:
                products_info += """
                    AND p.product_category_id = %(category)s
                """

            # 그룹바이 위치
            products_info += """
                GROUP BY p.id
            """
            # 정렬 코드 위치
            products_info += """
                ORDER BY p.id ASC
            """

            cursor.execute(products_info, filter_data)
            product_list = cursor.fetchall()
            total_count = len(product_list)

            # limit / offset 코드 위치
            if 'limit' and 'offset' in page_condition:
                limit = page_condition['limit']
                offset = page_condition['offset']
                products_info += f"""
                    LIMIT {limit}
                    OFFSET {offset}
                """

            cursor.execute(products_info, filter_data)
            product_list = cursor.fetchall()

        return {"data" : product_list, "limit" : limit}