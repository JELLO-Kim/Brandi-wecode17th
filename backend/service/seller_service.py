from flask import jsonify
from model.seller_dao import SellerDao
from responses import *


class SellerService:
    def post_product_with_discount(self, product_info, connection):
        seller_dao = SellerDao()
        if product_info['isDiscount'] == 1:
            if 'discountStart' and 'discountEnd' and 'discountPrice' and 'discountRate' not in product_info:
                raise ApiException(400, DISCOUNT_KEYS_NOT_IN_DATA)
            new_product_with_discount = seller_dao.post_product_with_discount(product_info, connection)
            return new_product_with_discount
        new_product = seller_dao.post_product
        return new_product
