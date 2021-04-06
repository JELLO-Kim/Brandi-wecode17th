import pymysql

from flask import jsonify
from responses import *

class MasterDao:

	def seller_type(self, connection):
		""" [어드민] 샐러 계정 관리(마스터) - 초기값
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            result : 샐러 타입 값
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
		""" [어드민] 샐러 계정 관리(마스터) - 초기값
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            result : 샐러 상태 값
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
		""" [어드민] 샐러 계정 관리(마스터) - 초기값
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            result : 샐러 속성 값
        """
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
	def master_find_seller_info(self, user, connection):
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			find_info = """
				SELECT
					s.image_url
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
	"""
	주석 추가 (# 필수입력 정보가 모두 작성되있던 상태에서 일부 값들을 수정할 경우(매니저 제외)) RESTFUL
	"""
	def master_update_information(self, seller_edit_info, connection):
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

	def account(self, connection, page_condition, filters):
		""" [어드민] 샐러 계정 관리(마스터) - 데이터 리스트
        Author: 
            Sung joun Jang
        Args:    
            - limit           : 페이지당 보여질 데이터 갯수
            - offset          : 현재 페이지
            - no              : 샐러의 no
            - username        : 샐러 id
            - english         : 브랜드의 영어 이름
            - korean          : 브랜드의 한글 이름
            - sellerType      : 샐러의 타입(일반, 헬피)
            - sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
            - sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
            - managerName     : 매니저의 이름
            - managerPhone    : 매니저의 핸드폰 번호
            - managerEmail    : 매니저의 이메일
            - startDate       : 샐러 생성된 날짜의 시작 값
            - endDate         : 샐러 생성된 날짜의 끝 값
        Returns:
			account_list : 전달하는 데이터 값
        """

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
				LEFT JOIN user_info u
					ON s.user_info_id = u.id
				LEFT JOIN seller_tier_types st
					ON s.seller_tier_type_id = st.id
				LEFT JOIN managers m
					ON u.id = m.seller_id
				LEFT JOIN seller_level_types sl
					ON s.seller_level_type_id = sl.id
				LEFT JOIN seller_categories sc
					ON s.seller_category_id = sc.id
				WHERE
					(m.ordering = 1 or m.ordering is null)
			"""

			# filter에 관한 값들을 검사
			if filters['no']: 
				account_sql += """ 
					AND u.id = %(no)s 
				"""
			if filters['username']: 
				account_sql += """ 
					AND u.username = %(username)s 
				"""
			if filters['english']: 
				account_sql += """ 
					AND s.english_brand_name = %(english)s 
				"""
			if filters['korean']: 
				account_sql += """ 
					AND u.korean_brand_name = %(korean)s 
				"""
			if filters['seller_type']: 
				account_sql += """ 
					AND st.id = %(seller_type)s 
				"""
			if filters['seller_status']: 
				account_sql += """ 
					AND sl.id = %(seller_status)s 
				"""
			if filters['seller_attribute']: 
				account_sql += """ 
					AND sc.id = %(seller_attribute)s 
				"""
			if filters['manager_name']: 
				account_sql += """ 
					AND m.name = %(manager_name)s 
				"""
			if filters['manager_phone']: 
				account_sql += """ 
					AND m.phone_number = %(manager_phone)s 
				"""
			if filters['manager_email']: 
				account_sql += """ 
					AND m.email = %(manager_email)s 
				"""
			# 날짜의 경우 start_date, end_date가 둘 다 넘어온다고 가정하고 between으로 처리
			if filters['start_date'] and filters['end_date']:
				account_sql += """ 
					AND (created_at BETWEEN %(start_date)s 
					AND %(end_date)s) 
				"""

			# 목록에 대한 limit & offset 설정
			account_sql += """
					LIMIT %(limit)s
					OFFSET %(offset)s
			"""

			cursor.execute(account_sql, {
				'limit'            : page_condition['limit'], 
				'offset'           : page_condition['offset'],
				'no'               : filters['no'],
				'username'         : filters['username'],
				'english'          : filters['english'],
				'korean'           : filters['korean'],
				'seller_type'      : filters['seller_type'],
				'seller_status'    : filters['seller_status'],
				'seller_attribute' : filters['seller_attribute'],
				'manager_name'     : filters['manager_name'],
				'manager_phone'    : filters['manager_phone'],
				'manager_email'    : filters['manager_email'],
				'start_date'       : filters['start_date'],
				'end_date'         : filters['end_date']
			})
			account_list = cursor.fetchall()
		
			return account_list
		
	def account_count(self, connection, filters):
		""" [어드민] 샐러 계정 관리(마스터) - 전체 개수
        Author: 
            Sung joun Jang
        Args:    
            - limit           : 페이지당 보여질 데이터 갯수
            - offset          : 현재 페이지
            - no              : 샐러의 no
            - username        : 샐러 id
            - english         : 브랜드의 영어 이름
            - korean          : 브랜드의 한글 이름
            - sellerType      : 샐러의 타입(일반, 헬피)
            - sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
            - sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
            - managerName     : 매니저의 이름
            - managerPhone    : 매니저의 핸드폰 번호
            - managerEmail    : 매니저의 이메일
            - startDate       : 샐러 생성된 날짜의 시작 값
            - endDate         : 샐러 생성된 날짜의 끝 값
        Returns:
			account_count : 전달하는 데이터 개수
        """

		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			account_count_sql = """
				SELECT 
					COUNT(*)
				FROM
					sellers s
				LEFT JOIN user_info u
					ON s.user_info_id = u.id
				LEFT JOIN seller_tier_types st
					ON s.seller_tier_type_id = st.id
				LEFT JOIN managers m
					ON u.id = m.seller_id
				LEFT JOIN seller_level_types sl
					ON s.seller_level_type_id = sl.id
				LEFT JOIN seller_categories sc
					ON s.seller_category_id = sc.id
				WHERE
					(m.ordering = 1 or m.ordering is null)
			"""

			# filter에 관한 값들을 검사
			if filters['no']: 
				account_count_sql += """ 
					AND u.id = %(no)s 
				"""
			if filters['username']: 
				account_count_sql += """ 
					AND u.username = %(username)s 
				"""
			if filters['english']: 
				account_count_sql += """ 
					AND s.english_brand_name = %(english)s 
				"""
			if filters['korean']: 
				account_count_sql += """ 
					AND u.korean_brand_name = %(korean)s 
				"""
			if filters['seller_type']: 
				account_count_sql += """ 
					AND st.id = %(seller_type)s 
				"""
			if filters['seller_status']: 
				account_count_sql += """ 
					AND sl.id = %(seller_status)s 
				"""
			if filters['seller_attribute']: 
				account_count_sql += """ 
					AND sc.id = %(seller_attribute)s 
				"""
			if filters['manager_name']: 
				account_count_sql += """ 
					AND m.name = %(manager_name)s 
				"""
			if filters['manager_phone']: 
				account_count_sql += """ 
					AND m.phone_number = %(manager_phone)s 
				"""
			if filters['manager_email']: 
				account_count_sql += """ 
					AND m.email = %(manager_email)s 
				"""
			# 날짜의 경우 start_date, end_date가 둘 다 넘어온다고 가정하고 between으로 처리
			if filters['start_date'] and filters['end_date']:
				account_count_sql += """ 
					AND (created_at BETWEEN %(start_date)s 
					AND %(end_date)s) 
				"""

			cursor.execute(account_count_sql, {
				'no'               : filters['no'],
				'username'         : filters['username'],
				'english'          : filters['english'],
				'korean'           : filters['korean'],
				'seller_type'      : filters['seller_type'],
				'seller_status'    : filters['seller_status'],
				'seller_attribute' : filters['seller_attribute'],
				'manager_name'     : filters['manager_name'],
				'manager_phone'    : filters['manager_phone'],
				'manager_email'    : filters['manager_email'],
				'start_date'       : filters['start_date'],
				'end_date'         : filters['end_date']
			})
			account_count = cursor.fetchone()
		
			return account_count

	def action(self, connection, level):
		""" [어드민] 샐러 계정 관리(마스터) - 액션 리스트
        Author: 
            Sung joun Jang
        Args:    
			- level: product_level의 name 값
        Returns:
            actions : 액션 리스트 데이터 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			action_sql = """
				SELECT 
					sa.name, sa.id
				FROM
					seller_action_types sa
				LEFT JOIN seller_level_types sl
					ON sa.seller_level_type_id = sl.id
				WHERE
					sl.name = %(level)s
			"""
			cursor.execute(action_sql, {'level': level})
			actions = cursor.fetchall()
		
			return actions

	def check_action_id(self, connection, action):
		""" [어드민] 샐러 계정 관리(마스터) - id로 넘어온 값을 name으로 반환
        Author: 
            Sung joun Jang
        Args:    
			- action : 액션의 id 값
        Returns:
			result: 액션의 name 값
        """
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
		""" [어드민] 샐러 계정 관리(마스터) - name으로 넘어온 값을 id로 반환
        Author: 
            Sung joun Jang
        Args:    
			- action : 액션의 name 값
        Returns:
			result: 액션의 id 값
        """
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
	
	def account_level(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - level 값 변경하기
        Author: 
            Sung joun Jang
        Args:    
			- seller_id : 샐러의 pk 값
        	- update_level : 변경할 level의 pk 값
        Returns:
			성공시 True
        """
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

	def account_level_log(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - level 값 변경하기(log)
        Author: 
            Sung joun Jang
        Args:    
			- seller_id : 샐러의 pk 값
        	- user_info_id : 변경한 user_id의 값
        Returns:
			성공시 True
        """
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

	def seller_delete(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - 퇴점 확정 시 soft delete
        Author: 
            Sung joun Jang
        Args:    
			- seller_id : 샐러의 pk 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				UPDATE
					sellers
				SET
					is_delete = 1
				WHERE
					user_info_id = %(user_info_id)s
			"""

			cursor.excute(sql, {'seller_id': data['seller_id']})
			
			return True
	
	def seller_delete_log(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - 퇴점 확정 시 soft delete(+ 내역 추가)
        Author: 
            Sung joun Jang
        Args:    
			- seller_id : 샐러의 pk 값
			- user_info_id : 유저의 pk 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				INSERT INTO
					seller_logs(
						user_info_id,
						seller_tier_type_id,
						seller_category_id,
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
		""" [어드민] 주문관리(마스터) - 상품준비(카테고리)
        Author: 
            Sung joun Jang
        Args:    

        Returns:
			result: 카테고리의 값
        """
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

	def order_ready(self, connection, filters, page_condition):
		""" [어드민] 주문관리(마스터) - 상품준비(검색값)
        Author: 
            Sung joun Jang
        Args:    
			- categories : 검색 하고자 하는 샐러 속성의 리스트 값
			- page_condition : 페이지에 대한 값들
        Returns:
			result: 카테고리의 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					u.user_info_id userInfoId,
					o.payment orderDate,
					o.order_number orderNumber,
					c.cart_number orderDetailNumber,
					s.korean_brand_name name,
					p.name productName,
					pc.name colorName,
					ps.name sizeName,
					po.additional_price additionalPrice,
					c.quantity,
					o.order_name orderName,
					o.order_phone orderPhone,
					o.total_price totalPrice,
					os.name orderStatus
				FROM
					orders o
				LEFT JOIN users u
					ON o.user_id = u.user_info_id
				LEFT JOIN carts c
					ON o.id = c.order_id
				LEFT JOIN product_options po
					ON c.product_option_id = po.id
				LEFT JOIN products p
					ON p.id = po.product_id
				LEFT JOIN sellers s
					ON s.user_info_id = p.seller_id
				LEFT JOIN product_color_types pc
					ON po.product_color_type_id = pc.id
				LEFT JOIN product_size_types ps
					ON po.product_size_type_id = ps.id
				LEFT JOIN order_status_types os
					ON o.order_status_type_id = os.id
				LEFT JOIN seller_categories sc
					ON s.seller_category_id = sc.id
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
				LIMIT %(limit)s
				OFFSET %(offset)s
			"""

			cursor.execute(sql, {
				'categories' : filters['categories'],
				'limit' : page_condition['limit'],
				'offset' : page_condition['offset']
			})
			result = cursor.fetchall()

			return result
	
	def order_ready_count(self, connection, filters):
		""" [어드민] 주문관리(마스터) - 상품준비(전체 데이터 개수)
        Author: 
            Sung joun Jang
        Args:    
			- categories : 검색 하고자 하는 샐러 속성의 리스트 값
			- page_condition : 페이지에 대한 값들
        Returns:
			result: 검색 결과의 데이터 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					COUNT(*)
				FROM
					orders o
				LEFT JOIN users u
					ON o.user_id = u.user_info_id
				LEFT JOIN carts c
					ON o.id = c.order_id
				LEFT JOIN product_options po
					ON c.product_option_id = po.id
				LEFT JOIN products p
					ON p.id = po.product_id
				LEFT JOIN sellers s
					ON s.user_info_id = p.seller_id
				LEFT JOIN product_color_types pc
					ON po.product_color_type_id = pc.id
				LEFT JOIN product_size_types ps
					ON po.product_size_type_id = ps.id
				LEFT JOIN order_status_types os
					ON o.order_status_type_id = os.id
				LEFT JOIN seller_categories sc
					ON s.seller_category_id = sc.id
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
		""" [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경)
        Author: 
            Sung joun Jang
        Args:    
			- categories : 검색 하고자 하는 샐러 속성의 리스트 값
        Returns:
			result: 검색 결과의 데이터 값
        """
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
		""" [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경 log)
        Author: 
            Sung joun Jang
        Args:    
			- user_id : 변경하는 유저의 pk 값
			- order_id : 변경하고자 하는 주문의 pk 값
        Returns:
			성공시 True
        """
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

	def order_detail(self, connection, product_id, cart_number):
		""" [어드민] 주문 상세 관리(마스터)
        Author: 
            Sung joun Jang
        Args:    
			- product_id : 조회하고자 하는 상품의 pk 값
			- cart_number : 조회하고자 하는 카트의 외부 고유 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					o.order_number orderNumber,
					o.payment orderDate,
					o.total_price totalPrice,
					c.cart_number cartNumber,
					o.payment cartDate,
					o.order_phone orderPhone,
					p.id productId,
					p.name productName,
					c.calculated_price discountPrice,
					pl.discount_rate discountRate,
					pl.price unitOriginalPrice,
					s.korean_brand_name brandName,
					pc.name colorName,
					ps.name sizeName,
					c.quantity,
					os.name orderStatus,
					u.user_info_id userNo,
					o.order_name orderName,
					si.recipient_name recipientName,
					si.recipient_phone recipientPhone,
					si.recipient_postal_code recipientPostalCode,
					si.recipient_address recipientAddress,
					si.recipient_address_detail recipientAddressDetail,
					sm.contents orderMessage
				FROM
					orders o
				LEFT JOIN users u
					ON o.user_id = u.user_info_id
				LEFT JOIN carts c
					ON o.id = c.order_id
				LEFT JOIN product_options po
					ON c.product_option_id = po.id
				LEFT JOIN products p
					ON p.id = po.product_id
				LEFT JOIN sellers s
					ON s.user_info_id = p.seller_id
				LEFT JOIN product_color_types pc
					ON po.product_color_type_id = pc.id
				LEFT JOIN product_size_types ps
					ON po.product_size_type_id = ps.id
				LEFT JOIN order_status_types os
					ON o.order_status_type_id = os.id
				LEFT JOIN seller_categories sc
					ON s.seller_category_id = sc.id
				LEFT JOIN shipping_info si
					ON o.shipping_info_id = si.id
				LEFT JOIN shipping_memo_types sm
					ON o.shipping_memo_type_id = sm.id
				LEFT JOIN product_logs pl
					ON pl.product_id = p.id
				WHERE
					pl.id = (
						SELECT 
							max(id) 
						FROM 
							product_logs
						WHERE 
							product_id = %(product_id)s AND change_date <= now()
						)
					AND
					c.cart_number = %(cart_number)s;
			"""

			cursor.execute(sql, {
				'cart_number' : cart_number,
				'product_id'  : product_id
			})
			result = cursor.fetchone()

			return result
	
	def order_detail_get_log(self, connection, cart_number):
		""" [어드민] 주문 상세 관리(마스터) - 로그
        Author: 
            Sung joun Jang
        Args:    
			- cart_number : 조회하고자 하는 카트의 외부 고유 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					ol.created_at createdAt, 
					os.name orderStatus
				FROM 
					order_logs ol
				LEFT JOIN carts c
					ON c.order_id = ol.order_id
				LEFT JOIN order_status_types os
					ON ol.order_status_type_id = os.id
				WHERE 
					ol.order_status_type_id > 1
					AND 
					c.cart_number = %(cart_number)s
			"""

			cursor.execute(sql, {'cart_number' : cart_number})
			result = cursor.fetchall()

			return result
