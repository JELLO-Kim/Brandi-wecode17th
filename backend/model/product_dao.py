from flask  import jsonify
from responses import *

import pymysql

class ProductDao:

    # category 정보
    def products_category(self, connection):
        """ [서비스] products의 category list
        Author
            : Chae hyun Kim
        Args
            : connection = 커넥션
        Returns 
            : category list
        """
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
    def products_list(self, connection, page_condition):
        """ [서비스] products의 category list
        Author
            : Chae hyun Kim
        Args
            : connection = 커넥션
            : page_condition = limit, offset, filtering 조건이 될 category 정보 
        Returns 
            : product list
        Note
            : filtering 될시 해당 조건에 부합하는 products 만 반환
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            products_info = """
                SELECT
                    p.id AS productId,
                    s.korean_brand_name AS sellerName,
                    name,
                    p.discount_rate AS discountRate,
                    p.price AS price,
                    p.discountPrice AS discountPrice,
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

            if 'category' in page_condition:
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

            cursor.execute(products_info, page_condition)
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

            cursor.execute(products_info, page_condition)

            return cursor.fetchall()

    def product_list_total_count(self, connection, page_condition):
        """ [서비스] product 총 갯수
        Author
            : Chae hyun Kim
        Args
            : connection = 커넥션
            : page_condition = iltering 조건이 될 category 정보 
        Returns 
            : product list 총 갯수
        Note
            : filtering 될시 해당 조건에 부합하는 products의 총 갯수로 반환
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            count_query = """
                SELECT
                    COUNT(*)
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

            if 'category' in page_condition:
                count_query += """
                    AND p.product_category_id = %(category)s
                """

            # 그룹바이 위치
            count_query += """
                GROUP BY p.id
            """
            cursor.execute(count_query, page_condition)
            return cursor.fetchone()


    def product_detail(self, product_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
				p.id,
                s.user_info_id AS sellerId,
                (
                    SELECT
                        GROUP_CONCAT(image_url ORDER BY ordering SEPARATOR ', ') 
                    FROM product_thumbnails
                    WHERE 
                        product_id=%(product_id)s
                ) AS imageList,
                s.korean_brand_name AS brand,
                p.name,
                p.price,
                p.discount_rate AS discountRate,
                p.discountPrice AS discountPrice,
                (
                    SELECT 
                        GROUP_CONCAT(DISTINCT CONCAT(ct.id, ':', name) ORDER BY ordering ASC)
                    FROM  
                        product_color_types AS ct 
                        INNER JOIN product_options AS po
                        ON ct.id = po.product_color_type_id 
                    WHERE 
                        product_id=%(product_id)s
                ) AS colors,
                (
                    SELECT 
                        GROUP_CONCAT(DISTINCT CONCAT(st.id, ':', name) ORDER BY ordering ASC) 
                    FROM 
                        product_size_types AS st
                        INNER JOIN product_options AS po
                        ON st.id = po.product_size_type_id 
                    WHERE 
                        product_id=%(product_id)s
                ) AS sizes,
                p.minimum,
                p.maximum,
                p.total_sales AS totalSales,
                p.contents_image AS productContentImage
            FROM
                user_info AS ui
            LEFT JOIN sellers AS s
                ON ui.id = s.user_info_id
            LEFT JOIN products AS p
                ON s.user_info_id = p.seller_id
            LEFT JOIN product_thumbnails AS pt
                ON p.id = pt.product_id
            LEFT JOIN product_options AS po
                ON p.id = po.product_id
            LEFT JOIN product_color_types AS ct
                ON po.product_color_type_id = ct.id
            LEFT JOIN product_size_types AS st
                ON po.product_size_type_id = st.id
            WHERE
                p.id = %(product_id)s
            AND
                p.is_display = 1
            """
            cursor.execute(query, {'product_id':product_id})
            product_list = cursor.fetchone()
            
            return product_list
    
    def get_product_question(self, info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            count = """
            SELECT 
                count(*)
            FROM 
                qnas AS q
            LEFT JOIN qnas AS self
                ON self.parent_id = q.id    
            LEFT JOIN sellers AS s
                ON self.writer_id = s.user_info_id
            INNER JOIN products AS p
                ON q.product_id = p.id
            INNER JOIN question_types AS qt
                ON q.question_type_id = qt.id
             INNER JOIN user_info AS ui
                ON q.writer_id = ui.id
            WHERE
                p.id = %(product_id)s
            AND
                q.parent_id is NULL
            """
            cursor.execute(count, info)
            total_count = cursor.fetchone()

            query = """
            SELECT 
                q.id,
                qt.name AS questionType,
                q.is_finished AS isFinished,
                IF(
                    %(user_id)s = q.writer_id OR q.is_private = 0, q.contents, "비밀글입니다."
                ) AS contents,
                ui.username,
                q.writer_id,
                q.parent_id,
                q.created_at AS createdAt,
                q.is_private AS isPrivate,
                IF(
                    %(user_id)s = q.writer_id, self.contents, "비밀글입니다."
                ) AS r_contents,
                self.parent_id AS r_parent_id,
                s.korean_brand_name AS brand,
                self.created_at AS r_createdAt
            FROM 
                qnas AS q
            LEFT JOIN qnas AS self
                ON self.parent_id = q.id    
            LEFT JOIN sellers AS s
                ON self.writer_id = s.user_info_id
            INNER JOIN products AS p
                ON q.product_id = p.id
            INNER JOIN question_types AS qt
                ON q.question_type_id = qt.id
            INNER JOIN user_info AS ui
                ON q.writer_id = ui.id
            WHERE
                p.id = %(product_id)s
            AND
                q.parent_id is NULL
            LIMIT %(limit)s
            OFFSET %(offset)s
            """
            cursor.execute(query, info)
            
            return {"qna" : cursor.fetchall(), "totalCount": total_count["count(*)"]}


    def get_question_open(self, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                qt.id,
                qt.name
            FROM
                question_types AS qt
            ORDER BY
                ordering ASC
            """
            cursor.execute(query)

            return cursor.fetchall()

    
    def post_product_qna(self, question_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            INSERT INTO qnas(
                product_id,
                writer_id,
                question_type_id,
                is_finished,
                is_private,
                created_at,
                updated_at,
                contents,
                is_delete
            ) VALUES (
                %(product_id)s,
                %(user_id)s,
                %(question_type_id)s,
                0,
                %(is_private)s,
                NOW(),
                NOW(),
                %(contents)s,
                0
            )
            """
            cursor.execute(query, question_info)

            return cursor.lastrowid


    def get_other_products(self, info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                s.korean_brand_name AS brand,
                p.name,
                p.price,
                p.discount_rate AS discountRate,
                p.discountPrice AS discountPrice
            FROM 
                products AS p
            LEFT JOIN sellers AS s
                ON p.seller_id = s.user_info_id
            WHERE p.seller_id = %(seller_id)s
                AND NOT(p.id = %(product_id)s)
            ORDER BY RAND()
            LIMIT 5
            """
            cursor.execute(query, info)

            return cursor.fetchall()