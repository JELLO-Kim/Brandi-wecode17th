import bcrypt
import jwt
from model.seller_dao import SellerDao
from model.user_dao import UserDao
from config import SECRET_KEY, ALGORITHM


class SellerService:
    def create_seller(self, seller_info, connection):
        user_dao = UserDao()
        seller_dao = SellerDao()
        is_existing_username = seller_dao.find_seller(seller_info, connection)
        if is_existing_username:
            raise ApiException('EXISTING_USERNAME')

        is_check_user_type = user_dao.seller_user_type_check(seller_info, connection)
        if not is_check_user_type == 'seller':
            raise ApiException('IS_NOT_SELLER')

        # 하나로 합치는거 해보기
        is_existing_korean_brand_name = user_dao.check_seller_korean_brand_name(seller_info, connection)
        if is_existing_korean_brand_name:
            raise ApiException('EXISTING_KOREAN_NAME')

        is_existing_english_brand_name = user_dao.check_seller_english_brand_name(seller_info, connection)
        if is_existing_english_brand_name:
            raise ApiException('EXISTING_ENGLISH_NAME')

        bcrypt_password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt())
        seller_info['password'] = bcrypt_password
        seller_id = user_dao.create_user_info(seller_info, connection)
        seller_info['user_info_id'] = seller_id
        seller_info['changer_id'] = seller_id
        user_dao.create_user_info_log(seller_info, connection)
        seller_info = {
            'korean_brand_name': seller_info,
            'english_brand_name': seller_info,
            'customer_service_number': seller_info,
            'seller_category_id': seller_info,
            'seller_tier_type_id': '',
            'seller_status_type_id': '',
            'seller_action_level_type_id': '',
            'seller_level_type_id': '',
            'saled_statistics_id': '',
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
            'is_weekend': '',
            'delivery_information': '',
            'refund_information': '',
        }
        # seller_info['korean_brand_name'] = seller_info
        # seller_info['english_brand_name'] = seller_info
        # seller_info['customer_service_number'] = seller_info
        # seller_info['seller_tier_type_id'] = ''
        # seller_info['seller_status_type_id'] = ''
        # seller_info['seller_level_type_id'] = ''
        # seller_info['salee_id'] = ''
        # seller_info['seller_status_type_id'] = ''
        # seller_info['seller_level_type_id'] = ''
        # seller_info['saled_statistics_id'] = ''
        # seller_info['customer_service_name'] = ''
        # seller_info['customer_service_opening'] = ''
        # seller_info['customer_service_closing'] = ''
        # seller_info['image_url'] = ''
        # seller_info['background_image_url'] = ''
        # seller_info['introduce'] = ''
        # seller_info['description'] = ''
        # seller_info['postal_code'] = ''
        # seller_info['address'] = ''
        # seller_info['address_detail'] = ''
        # seller_info['is_weekend'] = ''
        # seller_info['delivery_information'] = ''
        # seller_info['refund_information'] = ''
        seller_info_id = seller_dao.create_seller(seller_info, connection)
        seller_info['user_info_id'] = seller_info_id
        seller_info['changer_id'] = seller_info_id
        user_dao.create_seller_logs(seller_info, connection)

        return seller_id

    def login_seller(self, seller_login_info, connection):

        user_dao = UserDao()
        seller_dao = SellerDao()

        seller = seller_dao.login_seller(login_seller_info, connection)

        is_check_user_type = user_dao.seller_user_type_check(seller_info, connection)
        if not is_check_user_type == 'seller':
            raise ApiException('IS_NOT_SELLER')

        if seller:
            if bcrypt.checkpw(login_info['password'].encode('utf-8'), user['password'].encode('utf-8')):
                token = jwt.encode({'user_id': seller['id']}, SECRET_KEY, ALGORITHM)
                user_id = seller['id']
                return jsonify({'accessToken': token, 'userId': seller_id}), 201
            if user['is_delete'] == 1:
                raise ApiException(400, USER_NOT_FOUND)
            raise ApiException(400, PASSWORD_MISMATCH)
        raise ApiException(400, USER_NOT_FOUND)

    def post_product(self, product_info, product_options, connection):
        seller_dao = SellerDao()
        product_id = seller_dao.create_product(product_info, connection)
        product_info['product_id'] = product_id

        for product_option in product_options:
            product_info['product_color_id'] = product_option['colorId']
            product_info['product_size_id'] = product_option['sizeId']
            product_info['stock'] = product_option['stock']
            product_option_id = seller_dao.create_product_option(product_info, connection)
            product_info['product_option_id'] = product_option_id
            seller_dao.create_product_option_log(product_info, connection)

        product_thumbnail_id = seller_dao.create_product_thumbnail(product_info, connection)
        product_info['product_thumbnail_id'] = product_thumbnail_id
        seller_dao.create_product_thumbnail_log(product_info, connection)

        return product_id
