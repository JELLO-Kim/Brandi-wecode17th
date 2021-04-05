from flask import request, Blueprint, jsonify, g
from db_connector import connect_db
from responses import *
from utils import login_decorator
from service.seller_service import SellerService
from validators import validate_password


class SellerView:
    seller_app = Blueprint('seller_app', __name__, url_prefix='/seller')

    @seller_app.route('signup', methods=['POST'])
    def signup_seller():
        connection = None
        try:
            data = request.json

            if 'username' not in data:
                raise ApiException(400, INVALID_PASSWORD)
            if 'password' not in data:
                raise ApiException(400, INVALID_INPUT_USERNAME)
            if 'koreanBrandName' not in data:
                raise ApiException(400, INVALID_INPUT_PASSWORD)
            if 'englishBrandName' not in data:
                raise ApiException(400, INVALID_INPUT_ENGLISH_BRAND_NAME)
            if 'sellerCategoryId' not in data:
                raise ApiException(400, INVALID_INPUT_SELLER_CATEGORY)
            if 'customerServiceNumber' not in data:
                raise ApiException(400, INVALID_INPUT_SERVICE_NUMBER)
            if 'userTypeId' not in data:
                raise ApiException(400, INVALID_INPUT_USER_TYPE_ID)
            if 'phoneNumber' not in data:
                raise ApiException(400, INVALID_INPUT_PHONE_NUMBER)

            if not validate_password(data['password']):
                raise ApiException(400, INVALID_PASSWORD)

            seller_info = {
                'user_type_id': int(data['userTypeId']),
                'username': data['username'],
                'korean_brand_name': data['koreanBrandName'],
                'english_brand_name': data['englishBrandName'],
                'seller_category_id': data['sellerCategoryId'],
                'customer_service_number': data['customerServiceNumber'],
                'password': data['password'],
                'phone_number': data['phoneNumber'],
                'customer_service_name': '',
                'customer_service_opening': '',
                'customer_service_closing': '',
                'image_url': '',
                'background_image_url': '',
                'introduce': '',
                'description': '',
                'postal_code': '',
                'address': '',
                'address_detail': '',
                'delivery_information': '',
                'refund_information': ''
            }

            connection = connect_db()
            seller_service = SellerService()
            seller_service.signup_seller(seller_info, connection)
            connection.commit()

            return jsonify({'message': 'CREATED'}), 201

        except ApiException as e:
            connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @seller_app.route('signin', methods=['POST'])
    def signin_seller():
        connection = None
        try:
            data = request.json
            if 'username' not in data:
                raise ApiException(400, INVALID_PASSWORD)
            if 'password' not in data:
                raise ApiException(400, INVALID_INPUT_PASSWORD)

            seller_login_info = {
                'username': data['username'],
                'password': data['password']
            }

            connection = connect_db()
            seller_service = SellerService()
            seller_info = seller_service.signin_seller(seller_login_info, connection)
            connection.commit()

            return seller_info

        except ApiException as e:
            connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @seller_app.route('/edit', methods=['GET'])
    @login_decorator
    def seller_edit():
        """ [어드민] seller의 본인 정보 수정페이지 확인
        Author
            : Chae hyun Kim
        Args
            : token
        Returns
            : { "message"   : "SUCCESS"
                "result"    : {
                    "data" : 입력된 상세 정보}
                }
        Note
            : 회원가입 후 첫 수정페이지 입장 시 null 값이 존재함.
        """
        connection = None
        try:
            # user_id = g.token_info['user_id']
            # user_type_id = g.token_info['user_type_id']
            test_user_id = 26 # 다 채워져 있음
            # test_user_id = 33 # null 임
            user_type_id = 2
            if user_type_id == 2:
                user_id = test_user_id
            if user_type_id == 3:
                user_id = request.json()['sellerId']
            connection = connect_db()

            seller_service = SellerService()
            result = seller_service.seller_edit_get(user_id, connection)
            return {"data" : result}
        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

        return {"data" : result}

    @seller_app.route('/edit', methods=['PATCH'])
    @login_decorator
    def seller_account():
        """ [어드민] seller의 본인 정보 수정페이지 - 수정
        Author
            : Chae hyun Kim
        Args
            : token
        Returns
            : { "message"   : "SUCCESS"
                "result"    : {
                    "data" : 수정한 내역 갯수}
                }
        Note
            : 추가 입력 정보에 대한 값은 들어오면 들어온 값으로, 들어오지 않는다면 해당 key에는 None을 담는다
        """
        connection = None
        try:
            # user_id = g.token_info['user_id']
            # user_type_id = g.token_info['user_type_id']
            test_user_id = 26 # 다 채워져 있음
            # test_user_id = 33 # null 임
            user_type_id = 2
            if user_type_id == 2:
                user_id = test_user_id
            if user_type_id == 3:
                user_id = request.json()['sellerId']
            connection = connect_db()

            data = request.get_json()
            manager = data['manager'] if 'manager' in data else None
            if manager:
                for one_manager in manager:
                    one = {
                        "name" : one_manager['name'],
                        "email" : one_manager['email']
                    }

            seller_edit_info = {
                'profile'           : data.get('profile', None),
                'background_image'  : data.get('backgroundImage', None),
                'introduce'         : data.get('introduce', None),
                'description'       : data.get('detailDescription', None),
                'manager'           : data.get('manager', None),
                'call_number'       : data.get('callNumber', None),
                'callName'          : data.get('callName', None),
                'callStart'         : data.get('callStart', None),
                'callEnd'           : data.get('callEnd', None),
                'postalCode'        : data.get('postal', None),
                'address'           : data.get('address', None),
                'detailAddress'     : data.get('detailAddress', None),
                'delivery_info'     : data.get('shippingDescription', None),
                'refund_info'       : data.get('orderDescription', None),
                'is_weekend'        : data.get('isWeekend', None),
                'managers'          : data.get('managers', None)
            }

            seller_edit_info['user_id'] = str(user_id)
            print('user_id여깄자나!!!!!!!!!!!1', seller_edit_info['user_id'])

            seller_service = SellerService()
            result = seller_service.seller_edit_service(user_id, seller_edit_info, connection)

            connection.commit()
            return {"custom_message" : "update", "result" : "PATCH"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @seller_app.route('/edit', methods=['DELETE'])
    @login_decorator
    def seller_delete():
        """ [어드민] seller의 본인 정보 수정페이지 - 작성된 manager 정보 삭제
        Author
            : Chae hyun Kim
        Args
            : token
            : manager의 id
        Returns
            : { "message"   : "SUCCESS"
                "result"    : {
                    "data" : 삭제된 manager 정보}
                }
        """
        connection = None
        try:
            user_id = g.token_info['user_id']
            connection = connect_db()
            data = request.json()
            manager_id = data['managerId']

            seller_service = SellerService()
            result = seller_service.seller_edit_delete(user_id, connection)
            return {"data" : result}
        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

        return {"data" : result}

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

            product_options = data['productOptions']

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
                'maximum': data.get('maximum', ''),
                'discount_start': data.get('discountStart', ''),
                'discount_end': data.get('discountEnd', ''),
                'discount_price': data.get('discountPrice', ''),
                'discount_rate': data.get('discountRate', 0)
            }

            connection = connect_db()
            seller_service = SellerService()
            seller_service.post_product(product_info, product_options, connection)
            connection.commit()

            return {"custom_message": "PRODUCT CREATED", "result": "POST"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
