from flask import request, Blueprint, jsonify, g
from db_connector import connect_db
from responses import *
from utils import login_decorator
from service.seller_service import SellerService
from validators import validate_password
import traceback


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
                'phone_number': data['phoneNumber']
            }

            connection = connect_db()
            seller_service = SellerService()
            seller_service.signup_seller(seller_info, connection)
            connection.commit()

            return {"custom_message": "CREATED SELLER", "result": "POST"}

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
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

# 채현: get
    @seller_app.route('/edit', methods=['GET'])
    @login_decorator
    def seller_edit():
        """ [어드민] seller의 본인 정보 수정페이지 확인
        Author:
: Chae hyun Kim
        Args:
            - token(str): 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200:  
                { "message": "SUCCESS"
                    "result": {
                        "data": 입력된 상세 정보
                    }
                }
            - 400: 필수 parameter 미입력시 "** 정보를 입력해 주세요"
            - 403: 일반 user 접근 시 "일반 유저는 접근 권한이 없습니다"
        Note:
            - 회원가입 후 첫 수정페이지 입장 시 필수입력항목들에 null 값이 존재함.
        """
        connection = None
        try:
            user_type_id = g.token_info['user_type_id']
            if user_type_id == 1:
                raise ApiException(403, SERVICE_USER_NO_ACCESS)
            if user_type_id ==2:
                user = {
                    'user_id': g.token_info['user_id'],
                    'changer_id': g.token_info['user_id']
                }
            if user_type_id == 3:
                raise ApiException(403, ACCESS_DENIED)

            connection = connect_db()

            seller_service = SellerService()
            result = seller_service.seller_edit_get(user, connection)

            return {"data": result}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    # 채현: patch
    @seller_app.route('/edit', methods=['PATCH'])
    @login_decorator
    def seller_account():
        """ [어드민] seller의 본인 정보 수정페이지 - 수정
        Author:
            Chae hyun Kim
        Args:
            - token(str): 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200: { "message": "SUCCESS",
                            "result": {
                                "data": 수정한 내역 갯수
                                }
                            }
        Note:
            - 추가 입력 정보에 대한 값은 들어오면 들어온 값으로, 들어오지 않는다면 해당 key에는 None을 담는다
        """
        connection = None
        try:
            user_type_id = g.token_info['user_type_id']
            if user_type_id == 1:
                raise ApiException(403, SERVICE_USER_NO_ACCESS)
            if user_type_id ==2:
                user = {
                    'user_id': g.token_info['user_id'],
                    'changer_id': g.token_info['user_id'],
                    'user_type_id': g.token_info['user_type_id']
                }
            if user_type_id == 3:
                raise ApiException(403, ACCESS_DENIED)
                
            connection = connect_db()
            data = request.get_json()

            seller_edit_info = {
                'profile': data.get('profile', None),
                'background_image': data.get('backgroundImage', None),
                'introduce': data.get('introduce', None),
                'description': data.get('description', None),
                'call_number': data.get('customerServicePhone', None),
                'callName': data.get('customerServiceName', None),
                'callStart': data.get('customerServiceOpen', None),
                'callEnd': data.get('customerServiceClose', None),
                'postalCode': data.get('postal', None),
                'address': data.get('address', None),
                'detailAddress': data.get('addressDetail', None),
                'delivery_info': data.get('deliveryInfo', None),
                'refund_info': data.get('refundInfo', None),
                'is_weekend': data.get('isWeekend', 0),
                'brandKorean': data.get('brandKorean', None),
                'brandEnglish': data.get('brandEnglish', None),
                'managers': data.get('managers', None)
            }

            seller_edit_info['user_id'] = str(user['user_id'])
            seller_service = SellerService()
            result = seller_service.seller_edit_service(user, seller_edit_info, connection)

            connection.commit()

            return {"custom_message": UPDATED, "result": "PATCH"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

# 채현: delete
    @seller_app.route('/edit', methods=['DELETE'])
    @login_decorator
    def seller_delete():
        """ [어드민] seller의 본인 정보 수정페이지 - 작성된 manager 정보 삭제
        Author:
            Chae hyun Kim
        Args:
            - token(str): 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200: { "message": "SUCCESS",
                     "result": {
                         "data": 삭제된 manager 정보}
                    }
        """
        connection = None
        try:
            user_id = g.token_info['user_id']
            user_type_id = g.token_info['user_type_id']
            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)
            connection = connect_db()
            data = request.get_json()
            manager_id = data['managerId']
            extra = {
                'user_id': user_id,
                'user_type_id': user_type_id,
                'manager_id': manager_id
            }

            seller_service = SellerService()
            seller_service.seller_edit_delete(extra, connection)
            connection.commit()
            return {"custom_message": DELETED, "result": "DELETE"}
        
        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @seller_app.route('/product/management/init', methods=['GET'])
    @login_decorator
    def get_seller_product_page_info():
        """ [어드민] 셀러 상품 등록하기전에 선택할수있는 정보 (product_categories, product_sizes, product_colors) 뿌려주기
        Author:
            Mark Hasung Kim
        Returns:
            product_get_info (모든 product_categories, product_sizes, product_colors)
        """
        connection = None
        try:
            user_type_id = g.token_info['user_type_id']

            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)

            connection = connect_db()
            seller_service = SellerService()
            product_get_info = seller_service.get_product_post_info(connection)

            return product_get_info

        except ApiException as e:
            raise e
        finally:
            if connection:
                connection.close()

    @seller_app.route('/product/management/init', methods=['POST'])
    @login_decorator
    def post_seller_product():
        """ [어드민] 셀러 상품 등록
        Author:
            Mark Hasung Kim
        Returns:
            {
                    "custom_message": "PRODUCT_CREATED",
                    "result": "POST"
                    }
        """
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
            if 'productCategoryId' not in data:
                raise ApiException(400, PRODUCT_CATEGORY_NOT_IN_KEYS)
            if 'productName' not in data:
                raise ApiException(400, PRODUCT_NAME_NOT_IN_KEYS)
            if 'productThumbnailImages' not in data:
                raise ApiException(400, PRODUCT_THUMBNAIL_IMAGE_NOT_IN_KEYS)
            if 'productDetailImage' not in data:
                raise ApiException(400, PRODUCT_DETAIL_IMAGE_NOT_IN_KEYS)
            if 'price' not in data:
                raise ApiException(400, PRICE_NOT_IN_KEYS)
            if 'minimum' not in data:
                raise ApiException(400, PRODUCT_MINIMUM_NOT_IN_KEYS)
            if 'discountRate' not in data:
                raise ApiException(400, DISCOUNT_RATE_NOT_IN_KEYS)
            if 'productOptions' not in data:
                raise ApiException(400, PRODUCT_OPTION_NOT_IN_KEYS)
            if not data['productOptions']:
                raise ApiException(400, PRODUCT_OPTION_NOT_IN_INPUT)

            for product_option in data['productOptions']:
                if 'colorId' not in product_option:
                    raise ApiException(400, COLOR_NOT_IN_INPUT)
                if 'sizeId' not in product_option:
                    raise ApiException(400, SIZE_NOT_IN_INPUT)
                if 'stock' not in product_option:
                    raise ApiException(400, STOCK_NOT_IN_INPUT)

            product_thumbnail_images = data['productThumbnailImages']
            product_options = data['productOptions']

            product_info = {
                'user_id': user_id,
                'user_type_id': user_type_id,
                'is_selling': data['isSelling'],
                'is_display': data['isDisplay'],
                'product_category_id': data['productCategoryId'],
                'product_name': data['productName'],
                'product_detail_image': data['productDetailImage'],
                'price': data['price'],
                'discount_rate': data['discountRate'],
                'minimum': data['minimum'],
                'maximum': data.get('maximum', ''),
                'discount_start': data.get('discountStart', ''),
                'discount_end': data.get('discountEnd', ''),
                'discount_price': data.get('discountPrice', '')
            }

            if product_info['discount_rate'] == 0:
                product_info['is_discount'] = 0
            else:
                product_info['is_discount'] = 1

            connection = connect_db()
            seller_service = SellerService()
            product_id = seller_service.post_product(product_info, product_thumbnail_images, product_options, connection)
            connection.commit()

            return product_id

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @seller_app.route('/product/management/<int:product_id>', methods=['GET'])
    @login_decorator
    def get_seller_product_edit_info(product_id):
        """ [어드민] 상품 수정하기전에 보내줘야할 상품 정보 갖고오기
        Author:
            Mark Hasung Kim
        Args:
            product_id (url을 통해서 product_id를 받는다)
        Returns:
            product_edit_info (dict형식으로 상품의 디테일 정보, 모든 상품 카테고리, 컬러, 사이즈를 반환해준다)
        """
        connection = None
        try:
            user_id = g.token_info['user_id']
            user_type_id = g.token_info['user_type_id']

            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)

            product_info = {
                'user_id': user_id,
                'user_type_id': user_type_id,
                'product_id': product_id
            }

            connection = connect_db()
            seller_service = SellerService()
            default_product_info = seller_service.get_product_post_info(connection)
            product_edit_info = seller_service.get_product_edit_info(product_info, connection)
            product_edit_info['defaultInfo'] = default_product_info

            return product_edit_info

        except ApiException as e:
            raise e
        finally:
            if connection:
                connection.close()

    @seller_app.route('/product/management/<int:product_id>', methods=['PATCH'])
    @login_decorator
    def edit_seller_product(product_id):
        """ [어드민] 셀러 상품 수정
        Author:
            Mark Hasung Kim
        Returns:
            {
                'custom_message': 'PRODUCT_UPDATED',
                'result': 'PATCH'
                }
        """
        connection = None
        try:
            data = request.json
            user_id = g.token_info['user_id']
            user_type_id = g.token_info['user_type_id']

            if user_type_id != 2:
                raise ApiException(403, ACCESS_DENIED)

            product_info = {
                'user_id': user_id,
                'user_type_id': user_type_id,
                'product_id': product_id
            }
            product_options = None
            delete_product_options = None
            product_thumbnail_images = None
            delete_product_thumbnails = None

            if 'isSelling' in data:
                product_info['is_selling'] = data['isSelling']
            if 'isDisplay' in data:
                product_info['is_display'] = data['isDisplay']
            if 'productCategoryId' in data:
                product_info['product_category_id'] = data['productCategoryId']
            if 'productName' in data:
                product_info['product_name'] = data['productName']
            if 'productDetailImage' in data:
                product_info['product_detail_image'] = data['productDetailImage']
            if 'price' in data:
                product_info['price'] = data['price']
            if 'minimum' in data:
                product_info['minimum'] = data['minimum']
            if 'maximum' in data:
                product_info['maximum'] = data['maximum']

            if 'productOptions' in data:
                product_options = data['productOptions']
                for product_option in product_options:
                    if 'colorId' not in product_option:
                        raise ApiException(400, COLOR_NOT_IN_INPUT)
                    if 'sizeId' not in product_option:
                        raise ApiException(400, SIZE_NOT_IN_INPUT)
                    if 'stock' not in product_option:
                        raise ApiException(400, STOCK_NOT_IN_INPUT)

            if 'deleteProductOptions' in data:
                delete_product_options = data['deleteProductOptions']

            if 'productThumbnailImages' in data:
                product_thumbnail_images = data['productThumbnailImages']

            if 'deleteProductThumbnails' in data:
                delete_product_thumbnails = data['deleteProductThumbnails']

            if 'discountRate' in data:
                if data['discountRate'] != 0:
                    if 'discountPrice' not in data:
                        raise ApiException(400, DISCOUNT_PRICE_NOT_IN_KEYS)
                    if 'discountStart' not in data:
                        raise ApiException(400, DISCOUNT_START_NOT_IN_KEYS)
                    if 'discountEnd' not in data:
                        raise ApiException(400, DISCOUNT_END_NOT_IN_KEYS)
                    product_info['is_discount'] = 1
                    product_info['discount_price'] = data['discountPrice']
                    product_info['discount_start'] = data['discountStart']
                    product_info['discount_end'] = data['discountEnd']
                else:
                    product_info['is_discount'] = 0
                    product_info['discount_price'] = ''
                    product_info['discount_start'] = ''
                    product_info['discount_end'] = ''
                product_info['discount_rate'] = data['discountRate']

            if 'isDelete' in data:
                product_info['is_delete'] = 1

            connection = connect_db()
            seller_service = SellerService()
            seller_service.edit_product(
                product_info,
                product_options,
                delete_product_options,
                product_thumbnail_images,
                delete_product_thumbnails,
                connection
            )
            connection.commit()

            return {'custom_message': 'PRODUCT_UPDATED', 'result': 'PATCH'}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
