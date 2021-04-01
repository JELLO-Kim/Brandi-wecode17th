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
            data = request.json
            user_id = g.user_id
            user_type_id = g.user_type_id

            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)

            if 'isSelling' not in data:
                raise ApiException(400, IS_SELLING_NOT_IN_KEYS)
            if 'isDisplay' not in data:
                raise ApiException(400, IS_DISPLAY_NOT_IN_KEYS)
            if 'isDiscount' not in data:
                raise ApiException(400, IS_DISCOUNT_NOT_IN_KEYS)
            if 'category' not in data:
                raise ApiException(400, CATEGORY_NOT_IN_KEYS)
            if 'subCategory' not in data:
                raise ApiException(400, SUB_CATEGORY_NOT_IN_KEYS)
            if 'productExplanation' not in data:
                raise ApiException(400, PRODUCT_EXPLANATION_NOT_IN_KEYS)
            if 'productName' not in data:
                raise ApiException(400, PRODUCT_NAME_NOT_IN_KEYS)
            if 'productIntroduction' not in data:
                raise ApiException(400, PRODUCT_INTRODUCTION_NOT_IN_KEYS)
            if 'productThumbnailImage' not in data:
                raise ApiException(400, PRODUCT_THUMBNAIL_IMAGE_NOT_IN_KEYS)
            if 'productDetailImage' not in data:
                raise ApiException(400, PRODUCT_DETAIL_IMAGE_NOT_IN_KEYS)
            if 'productOption' not in data:
                raise ApiException(400, PRODUCT_OPTION_NOT_IN_KEYS)
            if 'price' not in data:
                raise ApiException(400, PRICE_NOT_IN_KEYS)
            if 'minimum' not in data:
                raise ApiException(400, PRODUCT_MINIMUM_NOT_IN_KEYS)

            product_info = {
                'user_id': user_id,
                'user_type_id': user_type_id,
                'is_selling': data['isSelling'],
                'is_display': data['isDisplay'],
                'is_discount': data['isDiscount'],
                'category': data['category'],
                'sub_category': data['subCategory'],
                'product_explanation': data['productExplanation'],
                'product_name': data['productName'],
                'product_introduction': data['productIntroduction'],
                'product_thumbnail_image': data['productThumbnailImage'],
                'product_detail_image': data['productDetailImage'],
                'product_option': data['productOption'],
                'price': data['price'],
                'minimum': data['minimum'],
                'maximum': data.get('maximum'),
                'discount_start': data.get('discountStart'),
                'discount_end': data.get('discountEnd'),
                'discount_price': data.get('discountPrice')
            }

            if not product_info['discount_start']:
                product_info['discount_start'] = ''
            if not product_info['discount_end']:
                product_info['discount_end'] = ''
            if not product_info['discount_price']:
                product_info['discount_price'] = ''
            if not product_info['maximum']:
                product_info['maximum'] = ''

            product_info['is_selling'] = data['isSelling']
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
