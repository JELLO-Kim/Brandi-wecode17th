from flask import request, Blueprint, jsonify, g
from db_connector import connect_db
from responses import *
from utils import login_decorator
from service.seller_service import SellerService


class SellerView:
    seller_app = Blueprint('seller_app', __name__)

    @seller_app.route('/product/management/edit', methods=['POST'])
    @login_decorator
    def post_seller_product():
        connection = None
        try:
            product_info = request.json
            user_id = g.user_id
            user_type_id = g.user_type_id
            product_info['user_id'] = user_id
            product_info['user_type_id'] = user_type_id

            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)

            if 'isSelling' not in product_info:
                raise ApiException(400, IS_SELLING_NOT_IN_KEYS)
            if 'isDisplay' not in product_info:
                raise ApiException(400, IS_DISPLAY_NOT_IN_KEYS)
            if 'isDiscount' not in product_info:
                raise ApiException(400, IS_DISCOUNT_NOT_IN_KEYS)
            if 'category' not in product_info:
                raise ApiException(400, CATEGORY_NOT_IN_KEYS)
            if 'subCategory' not in product_info:
                raise ApiException(400, SUB_CATEGORY_NOT_IN_KEYS)
            if 'productExplanation' not in product_info:
                raise ApiException(400, PRODUCT_EXPLANATION_NOT_IN_KEYS)
            if 'productName' not in product_info:
                raise ApiException(400, PRODUCT_NAME_NOT_IN_KEYS)
            if 'productIntroduction' not in product_info:
                raise ApiException(400, PRODUCT_INTRODUCTION_NOT_IN_KEYS)
            if 'productThumbnailImage' not in product_info:
                raise ApiException(400, PRODUCT_THUMBNAIL_IMAGE_NOT_IN_KEYS)
            if 'productDetailImage' not in product_info:
                raise ApiException(400, PRODUCT_DETAIL_IMAGE_NOT_IN_KEYS)
            if 'productOption' not in product_info:
                raise ApiException(400, PRODUCT_OPTION_NOT_IN_KEYS)
            if 'price' not in product_info:
                raise ApiException(400, PRICE_NOT_IN_KEYS)
            if 'minimum' not in product_info:
                raise ApiException(400, PRODUCT_MINIMUM_NOT_IN_KEYS)

            connection = connect_db()
            seller_service = SellerService()
            seller_service.post_product(product_info, connection)
            connection.commit()

            return jsonify({'MESSAGE': CREATED}), 201

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
