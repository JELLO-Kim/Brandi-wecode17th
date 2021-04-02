# from model.seller_dao import SellerDao
# from responses import *


# class SellerService:
#     def post_product(self, product_info, connection):
#         seller_dao = SellerDao()
#         if product_info['is_discount'] == 1:
#             if not 'discount_start' and not 'discount_end' and not 'discount_price' and not 'discount_rate':
#                 raise ApiException(400, DISCOUNT_KEYS_NOT_IN_DATA)
#             if product_info['maximum']:

#             new_product_with_discount = seller_dao.post_product_with_discount(product_info, connection)
#             return new_product_with_discount
#         else:
#             if product_info['maximum']:

#             new_product = seller_dao.post_product
#             return new_product
