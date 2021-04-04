import pymysql

from flask import jsonify
from responses import *

class MasterDao:

	def account(self, connection, page_condition, filters):
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
					m.ordering = 1 or m.ordering is null
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
					m.ordering = 1 or m.ordering is null
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
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			action_sql = """
				SELECT 
					sa.name, sa.id, sl.id
				FROM
					seller_action_types sa
				JOIN
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
					seller_level_type_id = %(update_action)s
				WHERE
					user_info_id = %(user_info_id)s
			"""

			cursor.execute(sql, {
				'update_action' : data['update_action'],
				'user_info_id'  : data['user_id']
			})

			return True

	def seller_delete(self, connection, data):
		with connection.cursor(pymysql.cursor.DictCursor) as cursor:
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