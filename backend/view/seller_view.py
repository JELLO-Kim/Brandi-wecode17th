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
            user_id = g.token_info['user_id']
            user_type_id = g.token_info['user_type_id']

            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)

            if 'isSelling' not in data:
                raise ApiException(400, IS_SELLING_NOT_IN_KEYS)
            if 'isDisplay' not in data:
                raise ApiException(400, IS_DISPLAY_NOT_IN_KEYS)
            if 'isDiscount' not in data:
                raise ApiException(400, IS_DISCOUNT_NOT_IN_KEYS)
            if 'productCategoryId' not in data:
                raise ApiException(400, PRODUCT_CATEGORY_NOT_IN_KEYS)
            if 'productName' not in data:
                raise ApiException(400, PRODUCT_NAME_NOT_IN_KEYS)
            if 'productThumbnailImage' not in data:
                raise ApiException(400, PRODUCT_THUMBNAIL_IMAGE_NOT_IN_KEYS)
            if 'productDetailImage' not in data:
                raise ApiException(400, PRODUCT_DETAIL_IMAGE_NOT_IN_KEYS)
            if 'productOptions' not in data:
                raise ApiException(400, PRODUCT_OPTION_NOT_IN_KEYS)
            if 'price' not in data:
                raise ApiException(400, PRICE_NOT_IN_KEYS)
            if 'minimum' not in data:
                raise ApiException(400, PRODUCT_MINIMUM_NOT_IN_KEYS)
            for product_option in data['productOptions']:
                if 'colorId' not in product_option:
                    raise ApiException(400, COLOR_NOT_IN_INPUT)
                if 'sizeId' not in product_option:
                    raise ApiException(400, SIZE_NOT_IN_INPUT)
                if 'stock' not in product_option:
                    raise ApiException(400, STOCK_NOT_IN_INPUT)

            product_info = {
                'user_id': user_id,
                'user_type_id': user_type_id,
                'is_selling': data['isSelling'],
                'is_display': data['isDisplay'],
                'is_discount': data['isDiscount'],
                'product_category_id': data['productCategoryId'],
                'product_name': data['productName'],
                'product_thumbnail_image': data['productThumbnailImage'],
                'product_detail_image': data['productDetailImage'],
                'price': data['price'],
                'minimum': data['minimum'],
                'maximum': data.get('maximum'),
                'discount_start': data.get('discountStart'),
                'discount_end': data.get('discountEnd'),
                'discount_price': data.get('discountPrice'),
                'discount_rate': data.get('discountRate')
            }

            if not product_info['discount_start']:
                product_info['discount_start'] = ''
            if not product_info['discount_end']:
                product_info['discount_end'] = ''
            if not product_info['discount_price']:
                product_info['discount_price'] = ''
            if not product_info['maximum']:
                product_info['maximum'] = ''
            if not product_info['discount_rate']:
                product_info['discount_rate'] = 0

            connection = connect_db()
            seller_service = SellerService()
            seller_service.post_product(product_info, product_options, connection)
            connection.commit()

            return jsonify({'message': CREATED}), 201

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
