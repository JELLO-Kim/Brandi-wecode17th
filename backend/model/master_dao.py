import pymysql

from flask import jsonify
from responses import *

class MasterDao:

  def account(self, connection, page_condition):
    limit = page_condition['limit']
    offset = page_condition['offset']

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
      account_sql = """
        SELECT 
          u.id as no,
          u.username as username,
          s.korean_brand_name as korean,
          s.english_brand_name as english,
          st.name as seller_type,
          m.name as manager,
          sl.name as seller_status,
          m.phone_number as phone,
          m.email as email,
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

      # 질문 목록에 대한 limit & offset 설정
      account_sql += f"""
          LIMIT {limit}
          OFFSET {offset}
      """

      cursor.execute(account_sql)
      account_list = cursor.fetchall()
    
      return account_list
    
  def account_count(self, connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
      # 질문 목록들 (parent_id가 NULL인것들)
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

      cursor.execute(account_count_sql)
      account_count = cursor.fetchone()
    
      return account_count

  def action(self, connection, level):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
      action_sql = """
        SELECT 
          sa.name, sa.id
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
