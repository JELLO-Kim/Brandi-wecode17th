# import pymysql


# class SellerDao:
#     def post_product_with_discount(self, product_info, connection):
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             query = """
#                 INSERT INTO products(
#                     seller_id,
#                     product_category_id,
#                     name,
#                     discount_start,
#                     discount_end,
#                     discount_rate,
#                     price,
#                     discounted_price,
#                     contents_image,
#                     total_sales
#             """

#     def post_product_with_discount_maximum(self, product_info, connection):
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             query = """
#                 INSERT INTO products(
#                     seller_id,
#                     product_category_id,
#                     name,
#                     discount_start,
#                     discount_end,
#                     discount_rate,
#                     price,
#                     discounted_price,
#                     contents_image,
#                     total_sales
#             """

#     def post_product_without_discount(self, product_info, connection):
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             query = """
#                 INSERT INTO products(
#                     seller_id,
#                     product_category_id,
#                     name,
#                     discount_start,
#                     discount_end,
#                     discount_rate,
#                     price,
#                     discounted_price,
#                     contents_image,
#                     total_sales
#             """

#     def post_product_without_discount_maximum(self, product_info, connection):
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             query = """
#                 INSERT INTO products(
#                     seller_id,
#                     product_category_id,
#                     name,
#                     discount_start,
#                     discount_end,
#                     discount_rate,
#                     price,
#                     discounted_price,
#                     contents_image,
#                     total_sales
#             """
