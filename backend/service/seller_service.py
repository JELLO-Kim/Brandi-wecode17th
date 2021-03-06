import bcrypt
import jwt
from flask import jsonify
from model.seller_dao import SellerDao
from model.master_dao import MasterDao
from config import SECRET_KEY, ALGORITHM
from responses import *


class SellerService:
    def signup_seller(self, seller_info, connection):
        seller_dao = SellerDao()
        is_existing_username = seller_dao.find_seller_username(seller_info, connection)
        if is_existing_username:
            raise ApiException(400, DUPLICATED_USERNAME)

        is_existing_korean_brand_name = seller_dao.check_seller_korean_brand_name(seller_info, connection)
        if is_existing_korean_brand_name:
            raise ApiException(400, DUPLICATED_KOREAN_BRAND_NAME)

        is_existing_english_brand_name = seller_dao.check_seller_english_brand_name(seller_info, connection)
        if is_existing_english_brand_name:
            raise ApiException(400, DUPLICATED_ENGLISH_BRAND_NAME)

        bcrypt_password = bcrypt.hashpw(seller_info['password'].encode('utf-8'), bcrypt.gensalt())
        seller_info['password'] = bcrypt_password
        seller_id = seller_dao.create_seller_user_info(seller_info, connection)
        seller_info['user_info_id'] = seller_id
        seller_dao.create_seller_user_info_log(seller_info, connection)

        seller_dao.create_seller(seller_info, connection)
        seller_dao.create_seller_log(seller_info, connection)

        return seller_id

    def signin_seller(self, seller_login_info, connection):
        seller_dao = SellerDao()

        seller = seller_dao.login_seller(seller_login_info, connection)

        if seller['user_type_id'] not in [2, 3]:
            raise ApiException(400, IS_NOT_SELLER)

        if seller:
            if bcrypt.checkpw(seller_login_info['password'].encode('utf-8'), seller['password'].encode('utf-8')):
                token = jwt.encode({'user_id': seller['id']}, SECRET_KEY, ALGORITHM)
                user_id = seller['id']
                user_type_id = seller['user_type_id']
                return jsonify({'accessToken': token, 'userId': user_id, "userTypeId" : user_type_id}), 201

            if seller['is_delete'] == 1:
                raise ApiException(400, USER_NOT_FOUND)
            raise ApiException(400, PASSWORD_MISMATCH)
        raise ApiException(400, USER_NOT_FOUND)
    # ?????? : get
    def seller_edit_get(self, user, connection):
        """ [?????????] seller??? ?????? ?????? ???????????? ????????? ?????? ??? ???????????? ??????
        Author : Chae hyun Kim
        Args:
            connection : ?????????
            user_id : ????????? ????????? user_id
        Returns
            : seller??? ?????? ?????? ??????
        Note
            : n?????? ????????? ??? ?????? manager??? ?????? ???????????? manager?????? key??? ?????? ??????
        """
        seller_dao = SellerDao()
        seller_get_service = seller_dao.seller_edit_get_dao(user, connection)
        seller_get_service['managers'] = seller_dao.get_seller_manager(user, connection)

        return seller_get_service

    # ?????? : patch
    def seller_edit_service(self, user, seller_edit_info, connection):
        """ [?????????] seller??? ?????? ?????? ???????????? ????????? ?????? ??? ???????????? ??????
        Author: 
            Chae hyun Kim
        Args:
            connection : ?????????
            user_id : ????????? ????????? user_id
            seller_edit_info : ?????? ????????? ?????????
        Note
            1. ???????????? ??? ??? ?????? : first_update ??????
            2. ????????? ?????? ?????? ????????? ?????? : seconde_update ??????
            3. manager??? ????????? ???????????? ????????? ????????? ??? ????????? "??????"??? ?????? ??? for loop ??????
        """
        seller_dao = SellerDao()
        master_dao = MasterDao()

        # ???????????? seller??? ???????????? ?????? ?????? (????????? ??????????????? ??????????????? ???????????? ?????? ?????? null??? ??? string?????? ???????????? ??????)
        find_information = seller_dao.find_seller_info(user, connection)
        
        managers = None
        if 'managers' in seller_edit_info:
            managers = seller_edit_info.pop('managers')
            # ????????? manager?????? ????????? ?????? ?????? managers??? ????????? 3 ????????? ?????? ??????
            if managers is not None:
                if len(managers) > 3:
                    raise ApiException(400, MAX_LIMIT_MANAGER)
            SellerService().manager_service(user, {'managers': managers}, connection)
        # ???????????? ????????? None??? ????????? ??? ???????????? ??????. first_update??? ???????????? ?????? parameter?????? ????????????.
        if None in find_information.values():
            SellerService().first_update(user, seller_edit_info, connection)
        # ???????????? ????????? None??? ????????? ?????? ???????????? ?????? ??? ????????? ???????????? ?????? ????????? ??????. seconde_update??? ????????????.
        else:
            SellerService().seconde_update(user, seller_edit_info, connection)

    def first_update(self, user, seller_edit_info, connection):
        """ [?????????] seller??? ?????? ?????? ?????? ?????? : ???????????? ??? ??? ??????
        Author : Chae hyun Kim
        Args:
            connection : ?????????
            user_id : ????????? ????????? user_id
            seller_edit_info : ?????? ????????? ?????????
        Returns
            : True
        Note
            : ?????? ???????????? ?????? value??? None??? ?????? ???????????? error message ??????
        """
        seller_dao = SellerDao()
        if not seller_edit_info['profile']:
            raise ApiException(400, NOT_PROFILE)
        if not seller_edit_info['introduce']:
            raise ApiException(400, NOT_DESCRIPTION)
        if not seller_edit_info['callName']:
            raise ApiException(400, NOT_CALL_NAME)
        if not seller_edit_info['callStart']:
            raise ApiException(400, NOT_CALL_START)
        if not seller_edit_info['callEnd']:
            raise ApiException(400, NOT_CALL_END)
        if not seller_edit_info['postalCode']:
            raise ApiException(400, NOT_POSTAL)
        if not seller_edit_info['address']:
            raise ApiException(400, NOT_ADDRESS)
        if not seller_edit_info['detailAddress']:
            raise ApiException(400, NOT_DETAIL_ADDRESS)
        if not seller_edit_info['delivery_info']:
            raise ApiException(400, NOT_SHIPPING_DESCRIPTION)
        if not seller_edit_info['refund_info']:
            raise ApiException(400, NOT_ORDER_DESCRIPTION)

        # ?????? ??????????????? ????????? ??????????????? ?????? ?????? ??????????????? ????????? 10??? ????????? ??????
        if seller_edit_info['description']:
            if len(seller_edit_info['description']) < 10:
                raise ApiException(400, SHORT_INPUT_SELLER)

        # ??? ?????? ????????? ?????? ??????
        seller_dao.update_information(seller_edit_info, connection)
        seller_dao.create_seller_update_log(user, connection)
        # return ?????? ??? manager??? ?????????????????? count??? ??????
        check_manager_num = seller_dao.check_seller_manager_number(user, connection)
        if check_manager_num['totalCount'] == 0:
            raise ApiException(400, NOT_MANAGER)

        return True

    # ??? ??????????????? ?????? ?????? ??????????????? ?????? ?????????????????? ???????????? ?????? ????????? ????????? ??????        
    def seconde_update(self, user, seller_edit_info, connection):
        """ [?????????] seller??? ?????? ?????? ?????? ?????? : ???????????? ?????? ??? ????????? ??????(?????? ????????? ?????? ??????)
        Author : Chae hyun Kim
        Args:
            connection : ?????????
            user_id : ????????? ????????? user_id
            seller_edit_info : ?????? ????????? ????????? (dict ??????)
        Returns
            : True
        Note:
            1. ?????????????????? ?????? manager??? ?????? 3???????????? error message ??????
            2. ????????? ????????? manager??? ?????? ?????? ????????? ?????? insert??? ?????? update ??????
            3. manager??? ????????? ???????????? ????????? ????????? ??? ????????? "??????"??? ?????? ??? for loop ??????
        """
        seller_dao = SellerDao()

        # ?????? ??????????????? ?????? ????????? ?????? ??????????????? ????????? 10??? ????????? ??????
        if seller_edit_info['description']:
            if len(seller_edit_info['description']) < 10:
                raise ApiException(400, SHORT_INPUT_SELLER)

        seller_dao.update_information(seller_edit_info, connection)
        seller_dao.create_seller_update_log(user, connection)
        return True

    # manager ??????/??????/??????
    def manager_service(self, user, seller_edit_info, connection):
        seller_dao = SellerDao()

        # ?????? ???????????????
        for one_request_manager in seller_edit_info['managers']:
            if 'name' not in one_request_manager:
                raise ApiException(400, NOT_MANAGER_NAME)
            if 'phoneNumber' not in one_request_manager:
                raise ApiException(400, NOT_MANAGER_NUMBER)
            if 'email' not in one_request_manager:
                raise ApiException(400, NOT_MANAGER_EMAIL)
        # ?????? ??????????????? (????????? ?????? ?????? ??????)
        for one_request_manager in seller_edit_info['managers']:
            phone = list(filter(lambda d:d['phoneNumber'] == one_request_manager['phoneNumber'], seller_edit_info['managers']))
            if len(phone) > 1:
                raise ApiException(400, EXSISTING_MANAGER_PHONE)

        # ?????? ????????? ?????????
        db_managers = seller_dao.get_seller_manager(user, connection)
        # ?????? ?????? ?????? => ???????????? ???????????? ?????????(seller_edit_delete)
        for row in db_managers:
            find_manager = list(filter(lambda x:x['id'] == row['id'], seller_edit_info['managers']))
            if len(find_manager) == 0:
                one = {
                    'id' : row['id'],
                    'manager_id' : row['id'],
                    'user_id' : user['user_id'],
                    'changer_id' : user['changer_id']
                }
                SellerService().seller_edit_delete(one, connection)

        # ?????? ?????? ??????
        for one_request_manager in seller_edit_info['managers']:
            find_manager = list(filter(lambda x:x['id'] == one_request_manager['id'], db_managers))
            # ?????? ????????? ?????? ???????????? ?????????
            if len(find_manager) >= 1:
                one = {
                    'id': one_request_manager['id'],
                    'name': one_request_manager['name'],
                    'email': one_request_manager['email'],
                    'phoneNumber': one_request_manager['phoneNumber'],
                    'user_id': user['user_id'],
                    'changer_id' : user['changer_id']
                }                    
                seller_dao.update_manager(one, connection)
                seller_dao.create_manager_log(one, connection)            
        
        # ?????? ????????? ??????
        for one_request_manager in seller_edit_info['managers']:
            # ?????? ?????? ?????? soft_delete ?????? ?????? manager??? ?????? 3 ???????????? ?????? ??????
            check_manager_num = seller_dao.check_seller_manager_number(user, connection)
            if check_manager_num['totalCount'] >= 3:
                raise ApiException(400, MAX_LIMIT_MANAGER)
            # ????????? ID??? ?????? ?????? ??????
            if one_request_manager.get('id', None) is None:
                one = {
                    'name': one_request_manager['name'],
                    'email': one_request_manager['email'],
                    'phoneNumber': one_request_manager['phoneNumber'],
                    'user_id': user['user_id'],
                    'changer_id': user['changer_id']
                }                    
                one['id'] = seller_dao.insert_information_manager(one, connection)
                seller_dao.create_manager_log(one, connection)
        return True

    # ?????? : delete
    def seller_edit_delete(self, one, connection):
        """ [?????????] seller??? ?????? ?????? ?????? : manager ?????? (soft_delete)
        Author:
            Chae hyun Kim
        Args:
            - extra(dict) :

        """
        try:
            seller_dao = SellerDao()
            seller_dao.delete_manager_dao(one, connection)
            seller_dao.create_manager_log(one, connection)
            return True
        except ApiException as e:
            raise e

    def get_product_post_info(self, connection):
        """ [?????????] ?????? ?????? ?????????????????? ????????? ?????? (product_category, product_sizes, product_colors) ????????????)
        Author:
            Mark Hasung Kim
        Args:
            connection: ?????????
        Returns:
            product_get_info (product_categories, product_colors, product_sizes ??????)
        """
        try:
            seller_dao = SellerDao()
            product_categories = seller_dao.get_all_product_categories(connection)
            product_colors = seller_dao.get_all_product_colors(connection)
            product_sizes = seller_dao.get_all_product_sizes(connection)
            product_get_info = {
                'product_categories': product_categories,
                'product_colors': product_colors,
                'product_sizes': product_sizes
            }
            return product_get_info

        except Exception as e:
            raise e

    def post_product(self, product_info, product_thumbnail_images, product_options, connection):
        """ [?????????] ?????? ?????? ??????
        Author:
            Mark Hasung Kim
        Args:
            product_info (dict): ????????? ??????????????? ??????
            product_thumbnail_images (list)
            product_options (dict): ????????? ????????? ?????? ?????? (product_colors, product_sizes, product_stock)
            connection: ?????????
        Returns:
            data (?????? ????????? product id??? dict???????????? ???????????????)
        """
        try:
            seller_dao = SellerDao()

            product_id = seller_dao.create_product(product_info, connection)
            product_info['product_id'] = product_id
            seller_dao.create_product_log(product_info, connection)

            for product_option in product_options:
                product_info['product_color_id'] = product_option['colorId']
                product_info['product_size_id'] = product_option['sizeId']
                product_info['stock'] = product_option['stock']
                product_option_id = seller_dao.create_product_option(product_info, connection)
                product_info['product_option_id'] = product_option_id
                seller_dao.create_product_option_log(product_info, connection)

            for product_thumbnail_image in product_thumbnail_images:
                product_info['image_url'] = product_thumbnail_image
                product_thumbnail_id = seller_dao.create_new_product_thumbnail(product_info, connection)
                product_info['product_thumbnail_id'] = product_thumbnail_id
                seller_dao.create_product_thumbnail_log(product_info, connection)

            data = {'product_id': product_id}

            return data

        except ApiException as e:
            raise e

    def get_product_edit_info(self, product_info, connection):
        """ [?????????] ?????? ?????????????????? ??????????????? ?????? ?????? ????????????
        Author:
            Mark Hasung Kim
        Args:
            product_info: product_id??? ???????????? dict
            connection: ?????????
        Returns:
            product_details (????????? ???????????? ????????? ????????? dict???????????? ???????????????)
        """
        seller_dao = SellerDao()
        product_details = seller_dao.get_product_details(product_info, connection)
        product_thumbnails = seller_dao.get_product_thumbnails(product_info, connection)
        product_details['productThumbnails'] = product_thumbnails
        product_colors_sizes = seller_dao.get_product_colors_sizes(product_info, connection)
        product_details['productColorsSizes'] = product_colors_sizes

        return product_details

    def edit_product(
            self,
            product_info,
            product_options,
            delete_product_options,
            product_thumbnail_images,
            delete_product_thumbnails,
            connection
    ):
        """ [?????????] ?????? ?????? ??????
        Author:
            Mark Hasung Kim
        Args:
            product_info (dict): ????????? ??????????????? ??????
            product_options (dict): ????????? ????????? ?????? ?????? (product_colors, product_sizes, product_stock)
            delete_product_options (list)
            product_thumbnail_images (list)
            delete_product_thumbnails (list)
            connection: ?????????
        Returns:
            True (????????? ??????????????? ?????? ???????????? True??? ???????????????)
        """
        try:
            seller_dao = SellerDao()

            seller_dao.update_product(product_info, connection)
            seller_dao.create_product_log(product_info, connection)

            #?????? ?????? ????????? ????????????:
            if product_info.get('is_delete'):
                seller_dao.soft_delete_product(product_info, connection)
                seller_dao.create_product_log(product_info, connection)

            #?????? ?????? ?????? ????????? ????????????:
            if product_options:
                for product_option in product_options:
                    product_info['product_color_id'] = product_option['colorId']
                    product_info['product_size_id'] = product_option['sizeId']
                    product_info['stock'] = product_option['stock']
                    product_option_id = seller_dao.create_product_option(product_info, connection)
                    product_info['product_option_id'] = product_option_id
                    seller_dao.create_product_option_log(product_info, connection)

            #?????? ?????? ?????? ????????? ????????????:
            if delete_product_options:
                for delete_product_option in delete_product_options:
                    product_info['product_option_id'] = delete_product_option
                    check_product_option = seller_dao.check_product_option(product_info, connection)
                    if check_product_option:
                        seller_dao.soft_delete_product_option(product_info, connection)
                        seller_dao.create_product_option_log(product_info, connection)
                    else:
                        raise ApiException(400, PRODUCT_OPTION_DOES_NOT_EXIST)

            #?????? thumbnail????????? ?????? ????????? ????????????:
            if product_thumbnail_images:
                for product_thumbnail_image in product_thumbnail_images:
                    product_info['image_url'] = product_thumbnail_image
                    product_thumbnail_id = seller_dao.create_new_product_thumbnail(product_info, connection)
                    product_info['product_thumbnail_id'] = product_thumbnail_id
                    seller_dao.create_product_thumbnail_log(product_info, connection)

            #?????? thumbnail????????? ?????? ????????? ????????????:
            if delete_product_thumbnails:
                for delete_product_thumbnail in delete_product_thumbnails:
                    product_info['product_thumbnail_id'] = delete_product_thumbnail
                    check_product_thumbnail = seller_dao.check_product_thumbnail(product_info, connection)
                    if check_product_thumbnail:
                        seller_dao.soft_delete_product_thumbnail(product_info, connection)
                        seller_dao.create_product_thumbnail_log(product_info, connection)
                    else:
                        raise ApiException(400, PRODUCT_THUMBNAIL_DOES_NOT_EXIST)

            return True

        except ApiException as e:
            raise e
