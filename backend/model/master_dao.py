import pymysql


class MasterDao:

	def seller_type(self, connection):
		""" [어드민] 샐러 계정 관리(마스터) - 초기값
        Author: 
            Sung joun Jang
        Args:    

        Returns:
            result: 샐러 타입 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					stt.id, stt.name
				FROM
					seller_tier_types AS stt
				ORDER BY
					stt.id ASC
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
            result: 샐러 상태 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					slt.id, slt.name
				FROM
					seller_level_types AS slt
				ORDER BY
					slt.id ASC
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
            result: 샐러 속성 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					sc.id, sc.name
				FROM
					seller_categories AS sc
				ORDER BY
					sc.id ASC
			"""

			cursor.execute(sql)
			result = cursor.fetchall()
		
			return result

	def account(self, connection, filters):
		""" [어드민] 샐러 계정 관리(마스터) - 데이터 리스트
        Author: 
            Sung joun Jang
        Args:    
            - limit: 페이지당 보여질 데이터 갯수
            - offset: 현재 페이지
            - no: 샐러의 no
            - username: 샐러 id
            - english: 브랜드의 영어 이름
            - korean: 브랜드의 한글 이름
            - sellerType: 샐러의 타입(일반, 헬피)
            - sellerStatus: 샐러의 상태(입점, 입점대기 등등)
            - sellerAttribute: 샐러의 속성(쇼핑몰, 뷰티 등등)
            - managerName: 매니저의 이름
            - managerPhone: 매니저의 핸드폰 번호
            - managerEmail: 매니저의 이메일
            - startDate: 샐러 생성된 날짜의 시작 값
            - endDate: 샐러 생성된 날짜의 끝 값
        Returns:
			account_list: 전달하는 데이터 값
        """

		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			account_sql = """
				SELECT 
					u.id AS no,
					u.username,
					s.korean_brand_name AS korean,
					s.english_brand_name AS english,
					st.name AS seller_type,
					m.name AS manager,
					sl.name AS seller_status,
					m.phone_number AS phone,
					m.email,
					sc.name AS attribute,
					s.created_at AS created
				FROM
					sellers AS s
				LEFT JOIN user_info AS u
					ON s.user_info_id = u.id
				LEFT JOIN seller_tier_types AS st
					ON s.seller_tier_type_id = st.id
				LEFT JOIN managers AS m
					ON u.id = m.seller_id
				LEFT JOIN seller_level_types AS sl
					ON s.seller_level_type_id = sl.id
				LEFT JOIN seller_categories AS sc
					ON s.seller_category_id = sc.id
				WHERE
					m.ordering = 1
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
					AND (
						s.created_at 
						BETWEEN 
							%(start_date)s 
						AND 
						DATE_ADD(
							%(end_date)s, INTERVAL 1 DAY
						)
					)
				"""

			# 목록에 대한 limit & offset 설정
			account_sql += """
					LIMIT %(limit)s
					OFFSET %(offset)s
			"""

			cursor.execute(account_sql, filters)
			account_list = cursor.fetchall()
		
			return account_list
		
	def account_count(self, connection, filters):
		""" [어드민] 샐러 계정 관리(마스터) - 전체 개수
        Author: 
            Sung joun Jang
        Args:    
            - limit: 페이지당 보여질 데이터 갯수
            - offset: 현재 페이지
            - no: 샐러의 no
            - username: 샐러 id
            - english: 브랜드의 영어 이름
            - korean: 브랜드의 한글 이름
            - sellerType: 샐러의 타입(일반, 헬피)
            - sellerStatus: 샐러의 상태(입점, 입점대기 등등)
            - sellerAttribute: 샐러의 속성(쇼핑몰, 뷰티 등등)
            - managerName: 매니저의 이름
            - managerPhone: 매니저의 핸드폰 번호
            - managerEmail: 매니저의 이메일
            - startDate: 샐러 생성된 날짜의 시작 값
            - endDate: 샐러 생성된 날짜의 끝 값
        Returns:
			account_count: 전달하는 데이터 개수
        """

		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			account_count_sql = """
				SELECT 
					COUNT(*) AS totalCount
				FROM
					sellers AS s
				LEFT JOIN user_info AS u
					ON s.user_info_id = u.id
				LEFT JOIN seller_tier_types AS st
					ON s.seller_tier_type_id = st.id
				LEFT JOIN managers AS m
					ON u.id = m.seller_id
				LEFT JOIN seller_level_types AS sl
					ON s.seller_level_type_id = sl.id
				LEFT JOIN seller_categories AS sc
					ON s.seller_category_id = sc.id
				WHERE
					m.ordering = 1
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
					AND (
						s.created_at 
						BETWEEN 
							%(start_date)s 
						AND 
						DATE_ADD(
							%(end_date)s, INTERVAL 1 DAY
						)
					)
				"""

			cursor.execute(account_count_sql, filters)
			account_count = cursor.fetchone()
		
			return account_count

	def action(self, connection, level):
		""" [어드민] 샐러 계정 관리(마스터) - 액션 리스트
        Author: 
            Sung joun Jang
        Args:    
			- level: product_level의 name 값
        Returns:
            actions: 액션 리스트 데이터 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			action_sql = """
				SELECT 
					sa.name, sa.id
				FROM
					seller_action_types AS sa
				LEFT JOIN seller_level_types AS sl
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
			- action: 액션의 id 값
        Returns:
			result: 액션의 name 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					sa.name
				FROM
					seller_action_types AS sa
				WHERE
					sa.id = %(action)s
			"""

			cursor.execute(sql, {'action': action})
			result = cursor.fetchone()

			return result
	
	def check_action_name(self, connection, action):
		""" [어드민] 샐러 계정 관리(마스터) - name으로 넘어온 값을 id로 반환
        Author: 
            Sung joun Jang
        Args:    
			- action: 액션의 name 값
        Returns:
			result: 액션의 id 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					sl.id
				FROM
					seller_level_types AS sl
				WHERE
					sl.name = %(action)s
			"""

			cursor.execute(sql, {'action': action})
			result = cursor.fetchone()

			return result
	
	def account_level(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - level 값 변경하기
        Author: 
            Sung joun Jang
        Args:    
			- seller_id: 샐러의 pk 값
        	- update_level: 변경할 level의 pk 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				UPDATE
					sellers AS s
				SET
					s.seller_level_type_id = %(update_level)s
				WHERE
					s.user_info_id = %(seller_id)s
			"""

			cursor.execute(sql, data)

			return True

	def account_level_log(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - level 값 변경하기(log)
        Author: 
            Sung joun Jang
        Args:    
			- seller_id: 샐러의 pk 값
        	- user_info_id: 변경한 user_id의 값
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
					s.user_info_id,
					s.seller_tier_type_id,
					s.seller_category_id,
					s.seller_level_type_id,
					s.sales_statistics_id,
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
					s.user_info_id = %(seller_id)s
			"""

			cursor.execute(sql, data)

			return True

	def seller_delete(self, connection, data):
		""" [어드민] 샐러 계정 관리(마스터) - 퇴점 확정 시 soft delete
        Author: 
            Sung joun Jang
        Args:    
			- seller_id: 샐러의 pk 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				UPDATE
					sellers AS s
				SET
					s.is_delete = 1
				WHERE
					s.user_info_id = %(user_info_id)s
			"""

			cursor.excute(sql, data)
			
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
					sc.id, sc.name
				FROM
					seller_categories AS sc
				ORDER BY
					sc.id ASC
			"""

			cursor.execute(sql)
			result = cursor.fetchall()

			return result

	def order_ready(self, connection, filters):
		""" [어드민] 주문관리(마스터) - 상품준비(검색값)
        Author: 
            Sung joun Jang
        Args:    
			- categories: 검색 하고자 하는 샐러 속성의 리스트 값
			- page_condition: 페이지에 대한 값들
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
					AND sc.name in %(categories)s
				"""

			sql += """
				ORDER BY
					o.id ASC
				LIMIT %(limit)s
				OFFSET %(offset)s
			"""

			cursor.execute(sql, filters)
			result = cursor.fetchall()

			return result
	
	def order_ready_count(self, connection, filters):
		""" [어드민] 주문관리(마스터) - 상품준비(전체 데이터 개수)
        Author: 
            Sung joun Jang
        Args:    
			- categories: 검색 하고자 하는 샐러 속성의 리스트 값
			- page_condition: 페이지에 대한 값들
        Returns:
			result: 검색 결과의 데이터 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT
					COUNT(*) AS totalCount
				FROM
					orders AS o
				LEFT JOIN users AS u
					ON o.user_id = u.user_info_id
				LEFT JOIN carts AS c
					ON o.id = c.order_id
				LEFT JOIN product_options AS po
					ON c.product_option_id = po.id
				LEFT JOIN products AS p
					ON p.id = po.product_id
				LEFT JOIN sellers AS s
					ON s.user_info_id = p.seller_id
				LEFT JOIN product_color_types AS pc
					ON po.product_color_type_id = pc.id
				LEFT JOIN product_size_types AS ps
					ON po.product_size_type_id = ps.id
				LEFT JOIN order_status_types AS os
					ON o.order_status_type_id = os.id
				LEFT JOIN seller_categories AS sc
					ON s.seller_category_id = sc.id
				WHERE
					os.id = 2
			"""

			if filters['categories']:
				sql += """
					AND sc.name in %(categories)s
				"""

			sql += """
				ORDER BY
					o.id ASC
			"""

			cursor.execute(sql, filters)
			result = cursor.fetchone()

			return result

	def order_ready_update(self, connection, data):
		""" [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경)
        Author: 
            Sung joun Jang
        Args:    
			- categories: 검색 하고자 하는 샐러 속성의 리스트 값
        Returns:
			result: 검색 결과의 데이터 값
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			# TODO: cart_number를 받아서 수정하게 해주자!
			sql = """
				UPDATE
					orders AS o
				LEFT JOIN carts c
					ON o.id = c.order_id
				SET
					o.order_status_type_id = 3
				WHERE
					c.cart_number = %(cart_number)s
			"""

			cursor.execute(sql, data)

			return True

	def order_ready_update_log(self, connection, data):
		""" [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경 log)
        Author: 
            Sung joun Jang
        Args:    
			- user_id: 변경하는 유저의 pk 값
			- order_id: 변경하고자 하는 주문의 pk 값
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
					o.id,
					o.order_status_type_id,
					o.user_id,
					o.order_name,
					o.order_phone,
					o.order_email,
					o.shipping_info_id,
					o.shipping_memo_type_id,
					o.created_at,
					o.updated_at,
					o.total_price,
					o.order_number,
					o.payment,
					o.is_delete,
					%(user_id)s,
					now()
				FROM
					orders AS o
				WHERE
					id = (
						SELECT 
							c.order_id
						FROM
							carts AS c
						WHERE
							c.cart_number = %(cart_number)s
					)
			"""

			cursor.execute(sql, data)

			return True

	def order_detail(self, connection, cart_number):
		""" [어드민] 주문 상세 관리(마스터)
        Author: 
            Sung joun Jang
        Args:    
			- product_id: 조회하고자 하는 상품의 pk 값
			- cart_number: 조회하고자 하는 카트의 외부 고유 값
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
					orders AS o
				LEFT JOIN users AS u
					ON o.user_id = u.user_info_id
				LEFT JOIN carts AS c
					ON o.id = c.order_id
				LEFT JOIN product_options AS po
					ON c.product_option_id = po.id
				LEFT JOIN products AS p
					ON p.id = po.product_id
				LEFT JOIN sellers AS s
					ON s.user_info_id = p.seller_id
				LEFT JOIN product_color_types AS pc
					ON po.product_color_type_id = pc.id
				LEFT JOIN product_size_types AS ps
					ON po.product_size_type_id = ps.id
				LEFT JOIN order_status_types AS os
					ON o.order_status_type_id = os.id
				LEFT JOIN seller_categories AS sc
					ON s.seller_category_id = sc.id
				LEFT JOIN shipping_info AS si
					ON o.shipping_info_id = si.id
				LEFT JOIN shipping_memo_types AS sm
					ON o.shipping_memo_type_id = sm.id
				LEFT JOIN product_logs AS pl
					ON pl.product_id = p.id
				WHERE
					pl.id = (
						SELECT 
							MAX(id) 
						FROM 
							product_logs
						WHERE 
							product_id = (
								SELECT 
									po.product_id
								FROM 
									carts AS c
								LEFT JOIN product_options po
									ON po.id = c.product_option_id
								WHERE 
									c.cart_number = %(cart_number)s
							) 
							AND 
							change_date <= o.payment
						)
					AND
					c.cart_number = %(cart_number)s;
			"""

			cursor.execute(sql, {'cart_number': cart_number})
			result = cursor.fetchone()

			return result
	
	def order_detail_get_log(self, connection, cart_number):
		""" [어드민] 주문 상세 관리(마스터) - 로그
        Author: 
            Sung joun Jang
        Args:    
			- cart_number: 조회하고자 하는 카트의 외부 고유 값
        Returns:
			성공시 True
        """
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			sql = """
				SELECT 
					ol.created_at createdAt, 
					os.name orderStatus
				FROM 
					order_logs AS ol
				LEFT JOIN carts c
					ON c.order_id = ol.order_id
				LEFT JOIN order_status_types os
					ON ol.order_status_type_id = os.id
				WHERE 
					ol.order_status_type_id > 1
					AND 
					c.cart_number = %(cart_number)s
			"""

			cursor.execute(sql, {'cart_number': cart_number})
			result = cursor.fetchall()

			return result
