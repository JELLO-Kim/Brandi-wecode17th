import pymysql

from flask import jsonify
from responses import *

class MasterDao:

	def account(self, connection, page_condition, filters):
		""" 샐러 계정 관리(마스터) - 리스트
        Author  
            : Sung joun Jang
        Args:
			# page_condition
            limit           : 페이지당 보여질 데이터 갯수
            offset          : 현재 페이지
			# filters
            no              : 샐러의 no
            username        : 샐러 id
            english         : 브랜드의 영어 이름
            korean          : 브랜드의 한글 이름
            sellerType      : 샐러의 타입(일반, 헬피)
            sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
            sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
            managerName     : 매니저의 이름
            managerPhone    : 매니저의 핸드폰 번호
            managerEmail    : 매니저의 이메일
            startDate       : 샐러 생성된 날짜의 시작 값
            endDate         : 샐러 생성된 날짜의 끝 값
        Returns 
            {
                "message": 결과에 따른 메세지,
                "result": [
                    {
                        "actions": [
                            {
                                "id": 1,
                                "name": "입점 승인",
                                "sl.id": 2
                            },
                            {
                                "id": 2,
                                "name": "입점 거절",
                                "sl.id": 2
                            }
                        ],
                        "attribute": "로드샵",
                        "createdAt": "Fri, 03 Apr 2020 00:00:00 GMT",
                        "english": "nanauhh",
                        "korean": "우나나나",
                        "managerEmail": "t2@gmail.com",
                        "managerName": "담2",
                        "managerPhone": "010-2",
                        "no": 6,
                        "sellerStatus": "입점 대기",
                        "sellerType": "일반",
                        "username": "nana"
                    }
                ]
            }
        """
		# 페이지에 관련된 변수들
		limit = page_condition['limit']
		offset = page_condition['offset']

		# 필터에 관련된 변수들
		no               = filters['no']
		username         = filters['username']
		english          = filters['english']
		korean           = filters['korean']
		seller_type      = filters['seller_type']
		seller_status    = filters['seller_status']
		seller_attribute = filters['seller_attribute']
		manager_name     = filters['manager_name']
		manager_phone    = filters['manager_phone']
		manager_email    = filters['manager_email']
		start_date       = filters['start_date']
		end_date         = filters['end_date']

		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			account_sql = """
				SELECT 
					u.id as no,
					u.username,
					s.korean_brand_name as korean,
					s.english_brand_name as english,
					st.name as seller_type,
					m.name as manager,
					sl.name as seller_status,
					m.phone_number as phone,
					m.email,
					sc.name as attribute,
					s.created_at as created
				FROM
					sellers s
				LEFT JOIN
					user_info u
					ON
						s.user_info_id = u.id
				LEFT JOIN
					seller_tier_types st
					ON
						s.seller_tier_type_id = st.id
				LEFT JOIN
					managers m
					ON
						u.id = m.seller_id
				LEFT JOIN
					seller_level_types sl
					ON
						s.seller_level_type_id = sl.id
				LEFT JOIN
					seller_categories sc
					ON
						s.seller_category_id = sc.id
				WHERE
					(m.ordering = 1 or m.ordering is null)
			"""

			# filter에 관한 값들을 검사
			if no: 
				account_sql += """ AND u.id = %(no)s """
			if username: 
				account_sql += """ AND u.username = %(username)s """
			if english: 
				account_sql += """ AND s.english_brand_name = %(english)s """
			if korean: 
				account_sql += """ AND u.korean_brand_name = %(korean)s """
			if seller_type: 
				account_sql += """ AND st.id = %(seller_type)s """
			if seller_status: 
				account_sql += """ AND sl.id = %(seller_status)s """
			if seller_attribute: 
				account_sql += """ AND sc.id = %(seller_attribute)s """
			if manager_name: 
				account_sql += """ AND m.name = %(manager_name)s """
			if manager_phone: 
				account_sql += """ AND m.phone_number = %(manager_phone)s """
			if manager_email: 
				account_sql += """ AND m.email = %(manager_email)s """
			# 날짜의 경우 start_date, end_date가 둘 다 넘어온다고 가정하고 between으로 처리
			if start_date and end_date:
				account_sql += """ AND (created_at BETWEEN %(start_date)s AND %(end_date)s) """

			# 질문 목록에 대한 limit & offset 설정
			account_sql += """
					LIMIT %(limit)s
					OFFSET %(offset)s
			"""

			cursor.execute(account_sql, {
				'limit'            : limit, 
				'offset'           : offset,
				'no'               : no,
				'username'         : username,
				'english'          : english,
				'korean'           : korean,
				'seller_type'      : seller_type,
				'seller_status'    : seller_status,
				'seller_attribute' : seller_attribute,
				'manager_name'     : manager_name,
				'manager_phone'    : manager_phone,
				'manager_email'    : manager_email,
				'start_date'       : start_date,
				'end_date'         : end_date
			})
			account_list = cursor.fetchall()
		
			return account_list
		
	def account_count(self, connection, filters):
		""" 샐러 계정 관리(마스터) - 전체 데이터의 개수 출력
        Author  
            : Sung joun Jang
        Args:
			# page_condition
            limit           : 페이지당 보여질 데이터 갯수
            offset          : 현재 페이지
			# filters
            no              : 샐러의 no
            username        : 샐러 id
            english         : 브랜드의 영어 이름
            korean          : 브랜드의 한글 이름
            sellerType      : 샐러의 타입(일반, 헬피)
            sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
            sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
            managerName     : 매니저의 이름
            managerPhone    : 매니저의 핸드폰 번호
            managerEmail    : 매니저의 이메일
            startDate       : 샐러 생성된 날짜의 시작 값
            endDate         : 샐러 생성된 날짜의 끝 값
        Returns 
			4
        """

		with connection.cursor(pymysql.cursors.DictCursor) as cursor:

			# 필터에 관련된 변수들
			no               = filters['no']
			username         = filters['username']
			english          = filters['english']
			korean           = filters['korean']
			seller_type      = filters['seller_type']
			seller_status    = filters['seller_status']
			seller_attribute = filters['seller_attribute']
			manager_name     = filters['manager_name']
			manager_phone    = filters['manager_phone']
			manager_email    = filters['manager_email']
			start_date       = filters['start_date']
			end_date         = filters['end_date']

			account_count_sql = """
				SELECT 
					COUNT(*)
				FROM
					sellers s
				LEFT JOIN
					user_info u
					ON
						s.user_info_id = u.id
				LEFT JOIN
					seller_tier_types st
					ON
						s.seller_tier_type_id = st.id
				LEFT JOIN
					managers m
					ON
						u.id = m.seller_id
				LEFT JOIN
					seller_level_types sl
					ON
						s.seller_level_type_id = sl.id
				LEFT JOIN
					seller_categories sc
					ON
						s.seller_category_id = sc.id
				WHERE
					(m.ordering = 1 or m.ordering is null)
			"""

			# filter에 관한 값들을 검사
			if no: 
				account_count_sql += """ AND u.id = %(no)s """
			if username: 
				account_count_sql += """ AND u.username = %(username)s """
			if english: 
				account_count_sql += """ AND s.english_brand_name = %(english)s """
			if korean: 
				account_count_sql += """ AND u.korean_brand_name = %(korean)s """
			if seller_type: 
				account_count_sql += """ AND st.id = %(seller_type)s """
			if seller_status: 
				account_count_sql += """ AND sl.id = %(seller_status)s """
			if seller_attribute: 
				account_count_sql += """ AND sc.id = %(seller_attribute)s """
			if manager_name: 
				account_count_sql += """ AND m.name = %(manager_name)s """
			if manager_phone: 
				account_count_sql += """ AND m.phone_number = %(manager_phone)s """
			if manager_email: 
				account_count_sql += """ AND m.email = %(manager_email)s """
			# 날짜의 경우 start_date, end_date가 둘 다 넘어온다고 가정하고 between으로 처리
			if start_date and end_date:
				account_count_sql += """ AND (created_at BETWEEN %(start_date)s AND %(end_date)s) """

			cursor.execute(account_count_sql, {
				'no'               : no,
				'username'         : username,
				'english'          : english,
				'korean'           : korean,
				'seller_type'      : seller_type,
				'seller_status'    : seller_status,
				'seller_attribute' : seller_attribute,
				'manager_name'     : manager_name,
				'manager_phone'    : manager_phone,
				'manager_email'    : manager_email,
				'start_date'       : start_date,
				'end_date'         : end_date
			})
			account_count = cursor.fetchone()
		
			return account_count

	def action(self, connection, level):
		""" 샐러 계정 관리(마스터) - action에 대한 값을 출력하는 함수
        Author  
            : Sung joun Jang
        Args:
			# page_condition
            limit           : 페이지당 보여질 데이터 갯수
            offset          : 현재 페이지
			# filters
            no              : 샐러의 no
            username        : 샐러 id
            english         : 브랜드의 영어 이름
            korean          : 브랜드의 한글 이름
            sellerType      : 샐러의 타입(일반, 헬피)
            sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
            sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
            managerName     : 매니저의 이름
            managerPhone    : 매니저의 핸드폰 번호
            managerEmail    : 매니저의 이메일
            startDate       : 샐러 생성된 날짜의 시작 값
            endDate         : 샐러 생성된 날짜의 끝 값
        Returns 
            [{
				name: 브랜드네임,
				id: 1,
				id: 2
			}]
        """

		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			action_sql = """
				SELECT 
					sa.name, sa.id, sl.id
				FROM
					seller_action_types sa
				LEFT JOIN
					seller_level_types sl
					ON
						sa.seller_level_type_id = sl.id
				WHERE
					sl.name = %(level)s
			"""
			cursor.execute(action_sql, {'level': level})
			actions = cursor.fetchall()
		
			return actions
			
	def seller_type(self, connection):
		""" 샐러 계정 관리(마스터) - 리스트(초기값 중 샐러 타입 리스트)
        Author  
            : Sung joun Jang
        Args:

        Returns 
            [
				{
					id: 1,
					name: 일반
				},
				{
					id: 2,
					name: 헬피
				}
			]
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					id, name
				FROM
					seller_tier_types
				ORDER BY
					id ASC
			"""

			cursor.execute(sql)
			result = cursor.fetchall()
		
			return result
	
	def seller_status(self, connection):
		""" 샐러 계정 관리(마스터) - 리스트(초기값 중 샐러 상태 리스트)
        Author  
            : Sung joun Jang
        Args:

        Returns 
            [
				{
					id: 1,
					name: 입점
				},
				{
					id: 2,
					name: 입점 대기
				},
				...
			]
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					id, name
				FROM
					seller_level_types
				ORDER BY
					id ASC
			"""

			cursor.execute(sql)
			result = cursor.fetchall()
		
			return result
	
	def seller_attribute(self, connection):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					id, name
				FROM
					seller_categories
				ORDER BY
					id ASC
			"""

			cursor.execute(sql)
			result = cursor.fetchall()
		
			return result
	
	def account_level(self, connection, data):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				UPDATE
					sellers
				SET
					seller_level_type_id = %(update_level)s
				WHERE
					user_info_id = %(seller_id)s
			"""

			cursor.execute(sql, {
				'update_level' : data['update_level'],
				'seller_id'    : data['seller_id']
			})

			return True

	def seller_delete(self, connection, data):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				UPDATE
					seller
				SET
					is_delete = 1
				WHERE
					user_info_id = %(user_info_id)s
			"""

			cursor.excute(sql, {'user_info_id': data['user_id']})
			
			return True

	def check_action_id(self, connection, action):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					name
				FROM
					seller_action_types
				WHERE
					id = %(action)s
			"""

			cursor.execute(sql, {'action': action})
			result = cursor.fetchone()

			return result
	
	def check_action_name(self, connection, action):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					id
				FROM
					seller_level_types
				WHERE
					name = %(action)s
			"""

			cursor.execute(sql, {'action': action})
			result = cursor.fetchone()

			return result

	def account_level_log(self, connection, data):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				INSERT INTO
					seller_logs(
						seller_id,
						seller_tier_type_id,
						seller_category_id,
						seller_level_type_id,
						sales_statistics_id,
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
					user_info_id,
					seller_tier_type_id,
					seller_category_id,
					seller_level_type_id,
					sales_statistics_id,
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
					%(user_info_id)s,
					now()
				FROM
					sellers
				WHERE
					user_info_id = %(seller_id)s
			"""

			cursor.execute(sql, {
				'seller_id'    : data['seller_id'],
				'user_info_id' : data['user_id']
			})

			return True

	def seller_category(self, connection):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					id, name
				FROM
					seller_categories
				ORDER BY
					id ASC
			"""

			cursor.execute(sql)
			result = cursor.fetchall()

			return result

	def order_ready(self, connection, filters):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					u.user_info_id,
					o.payment order_date,
					o.order_number,
					c.cart_number order_detail_number,
					s.korean_brand_name name,
					p.name product_name,
					pc.name color_name,
					ps.name size_name,
					po.additional_price,
					c.quantity,
					o.order_name,
					o.order_phone,
					o.total_price,
					os.name order_status
				FROM
					orders o
				LEFT JOIN
					users u
					ON
						o.user_id = u.user_info_id
				LEFT JOIN
					carts c
					ON
						o.id = c.order_id
				LEFT JOIN
					product_options po
					ON
						c.product_option_id = po.id
				LEFT JOIN
					products p
					ON
						p.id = po.product_id
				LEFT JOIN
					sellers s
					ON
						s.user_info_id = p.seller_id
				LEFT JOIN
					product_color_types pc
					ON
						po.product_color_type_id = pc.id
				LEFT JOIN
					product_size_types ps
					ON
						po.product_size_type_id = ps.id
				LEFT JOIN
					order_status_types os
					ON
						o.order_status_type_id = os.id
				LEFT JOIN
					seller_categories sc
					ON
						s.seller_category_id = sc.id
				WHERE
					os.id = 2
			"""

			if filters['categories']:
				sql += """
					AND
						sc.name in %(categories)s
				"""

			sql += """
				ORDER BY
					o.id ASC
			"""

			cursor.execute(sql, {
				'categories' : filters['categories']
			})
			result = cursor.fetchall()

			return result
	
	def order_ready_count(self, connection, filters):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					COUNT(*)
				FROM
					orders o
				LEFT JOIN
					users u
					ON
						o.user_id = u.user_info_id
				LEFT JOIN
					carts c
					ON
						o.id = c.order_id
				LEFT JOIN
					product_options po
					ON
						c.product_option_id = po.id
				LEFT JOIN
					products p
					ON
						p.id = po.product_id
				LEFT JOIN
					sellers s
					ON
						s.user_info_id = p.seller_id
				LEFT JOIN
					product_color_types pc
					ON
						po.product_color_type_id = pc.id
				LEFT JOIN
					product_size_types ps
					ON
						po.product_size_type_id = ps.id
				LEFT JOIN
					order_status_types os
					ON
						o.order_status_type_id = os.id
				LEFT JOIN
					seller_categories sc
					ON
						s.seller_category_id = sc.id
				WHERE
					os.id = 2
			"""

			if filters['categories']:
				sql += """
					AND
						sc.name in %(categories)s
				"""

			sql += """
				ORDER BY
					o.id ASC
			"""

			cursor.execute(sql, {
				'categories' : filters['categories']
			})
			result = cursor.fetchone()

			return result

	def order_ready_update(self, connection, data):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				UPDATE
					orders
				SET
					order_status_type_id = 3
				WHERE
					id = %(order_id)s
			"""

			cursor.execute(sql, {'order_id' : data['order_id']})

			return True

	def order_ready_update_log(self, connection, data):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				INSERT INTO
					order_logs(
						order_id,
						order_status_type_id,
						user_id,
						order_name,
						order_phone,
						order_email,
						shipping_info_id,
						shipping_memo_type_id,
						created_at,
						updated_at,
						total_price,
						order_number,
						payment,
						is_delete,
						changer_id,
						change_date
					)
				SELECT
					id,
					order_status_type_id,
					user_id,
					order_name,
					order_phone,
					order_email,
					shipping_info_id,
					shipping_memo_type_id,
					created_at,
					updated_at,
					total_price,
					order_number,
					payment,
					is_delete,
					%(user_id)s,
					now()
				FROM
					orders
				WHERE
					id = %(order_id)s
			"""

			cursor.execute(sql, data)

			return True