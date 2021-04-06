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
    # 채현 : get
    def seller_edit_get(self, user, connection):
        """ [어드민] seller의 본인 상세 정보수정 페이지 입장 시 확인되는 정보
        Author : Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
        Returns
            : seller의 상세 정보 반환
        Note
            : n개로 존재할 수 있는 manager에 대한 정보들은 manager라는 key값 안에 존재
        """
        seller_dao = SellerDao()
        seller_get_service = seller_dao.seller_edit_get_dao(user, connection)
        seller_get_service['managers'] = seller_dao.get_seller_manager(user, connection)

        return seller_get_service

    # 채현 : patch
    def seller_edit_service(self, user, seller_edit_info, connection):
        """ [어드민] seller의 본인 상세 정보수정 페이지 입장 시 확인되는 정보
        Author: 
            Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
            seller_edit_info : 새로 입력될 내용들
        Note
            1. 회원가입 후 첫 수정 : first_update 실행
            2. 첫번째 수정 이후 두번째 수정 : seconde_update 실행
            3. manager는 한번에 여러개의 정보를 입력할 수 있도록 "배열"로 받은 뒤 for loop 진행
        """
        seller_dao = SellerDao()
        master_dao = MasterDao()

        # 로그인한 seller의 추가정보 내용 확인 (첫번째 수정이라면 회원가입시 입력했던 정보 외에 null과 빈 string으로 처리되어 있음)
        find_information = seller_dao.find_seller_info(user, connection)
        
        managers = None
        if 'managers' in seller_edit_info:
            managers = seller_edit_info.pop('managers')
            # 들어온 manager들의 객체가 담긴 배열 managers의 길이가 3 초과면 에러 반환
            if managers is not None:
                if len(managers) > 3:
                    raise ApiException(400, MAX_LIMIT_MANAGER)
            SellerService().manager_service(user, {'managers': managers}, connection)
        # 필수입력 정보중 None이 있다면 첫 수정으로 간주. first_update로 보내지며 필수 parameter들이 요구된다.
        if None in find_information.values():
            SellerService().first_update(user, seller_edit_info, connection)
        # 필수입력 정보중 None이 없다면 이미 필수정보 입력 후 두번째 일부수정 가능 상태로 간주. seconde_update로 보내진다.
        else:
            SellerService().seconde_update(user, seller_edit_info, connection)

    def first_update(self, user, seller_edit_info, connection):
        """ [어드민] seller의 본인 상세 정보 수정 : 회원가입 후 첫 수정
        Author : Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
            seller_edit_info : 새로 입력될 내용들
        Returns
            : True
        Note
            : 필수 입력란에 대한 value가 None일 경우 해당하는 error message 반환
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

        # 선택 추가사항인 셀러의 상세소개에 대한 값이 들어왔지만 길이가 10자 미만일 경우
        if seller_edit_info['description']:
            if len(seller_edit_info['description']) < 10:
                raise ApiException(400, SHORT_INPUT_SELLER)

        # 첫 내용 기입과 이력 생성
        seller_dao.update_information(seller_edit_info, connection)
        seller_dao.create_seller_update_log(user, connection)
        # return 하기 전 manager도 생성되었는지 count로 확인
        check_manager_num = seller_dao.check_seller_manager_number(user, connection)
        if check_manager_num['totalCount'] == 0:
            raise ApiException(400, NOT_MANAGER)

        return True

    # 첫 수정페이지 작업 이후 필수값들이 모두 입력되어있는 상태에서 일부 값들만 수정할 경우        
    def seconde_update(self, user, seller_edit_info, connection):
        """ [어드민] seller의 본인 상세 정보 수정 : 필수정보 입력 후 두번째 수정(일부 내역만 수정 가능)
        Author : Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
            seller_edit_info : 새로 입력될 내용들 (dict 형태)
        Returns
            : True
        Note:
            1. 삭제되어있지 않은 manager가 이미 3명이라면 error message 반환
            2. 기존에 입력된 manager에 대한 정보 수정일 경우 insert가 아닌 update 진행
            3. manager는 한번에 여러개의 정보를 입력할 수 있도록 "배열"로 받은 뒤 for loop 진행
        """
        seller_dao = SellerDao()

        # 선택 추가사항인 새로 입력될 셀러 상세소개의 길이가 10자 미만일 경우
        if seller_edit_info['description']:
            if len(seller_edit_info['description']) < 10:
                raise ApiException(400, SHORT_INPUT_SELLER)

        seller_dao.update_information(seller_edit_info, connection)
        seller_dao.create_seller_update_log(user, connection)
        return True

    # manager 수정/삭제/생성
    def manager_service(self, user, seller_edit_info, connection):
        seller_dao = SellerDao()

        # 키값 벨리데이션
        for one_request_manager in seller_edit_info['managers']:
            if 'name' not in one_request_manager:
                raise ApiException(400, NOT_MANAGER_NAME)
            if 'phoneNumber' not in one_request_manager:
                raise ApiException(400, NOT_MANAGER_NUMBER)
            if 'email' not in one_request_manager:
                raise ApiException(400, NOT_MANAGER_EMAIL)
        # 중복 벨리데이션 (핸드폰 번호 중복 불허)
        for one_request_manager in seller_edit_info['managers']:
            phone = list(filter(lambda d:d['phoneNumber'] == one_request_manager['phoneNumber'], seller_edit_info['managers']))
            if len(phone) > 1:
                raise ApiException(400, EXSISTING_MANAGER_PHONE)

        # 기존 매니저 리스트
        db_managers = seller_dao.get_seller_manager(user, connection)
        # 삭제 대상 추림 => 삭제전용 메소드로 보내짐(seller_edit_delete)
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

        # 수정 대상 수정
        for one_request_manager in seller_edit_info['managers']:
            find_manager = list(filter(lambda x:x['id'] == one_request_manager['id'], db_managers))
            # 기존 매니저 요청 매니저가 일치함
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
        
        # 신규 대상을 추가
        for one_request_manager in seller_edit_info['managers']:
            # 추가 전에 이미 soft_delete 되지 않은 manager의 수가 3 이상이면 에러 반환
            check_manager_num = seller_dao.check_seller_manager_number(user, connection)
            if check_manager_num['totalCount'] >= 3:
                raise ApiException(400, MAX_LIMIT_MANAGER)
            # 신규는 ID가 전달 되지 않음
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

    # 채현 : delete
    def seller_edit_delete(self, one, connection):
        """ [어드민] seller의 상세 정보 수정 : manager 삭제 (soft_delete)
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
        """ 셀러 상품 등록하기전에 선택할 정보 (product_category, product_sizes, product_colors) 뿌려주기)
        Author: Mark Hasung Kim
        Args:
            connection: 커넥션
        Returns: product_get_info (product_categories, product_colors, product_sizes 정보)
        """
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

    def post_product(self, product_info, product_options, connection):
        """ 셀러 상품 등록
        Author: Mark Hasung Kim
        Args:
            product_info (dict): 등록할 상품에대한 정보
            product_options (dict): 등록할 상품의 옵션 정보 (product_colors, product_sizes, product_stock)
            connection: 커넥션
        Returns: product_id (새로 등록한 product id 반환해준다)
        """
        try:
            seller_dao = SellerDao()
            product_name_exists = seller_dao.check_existing_product_name(product_info, connection)

            if product_name_exists:
                raise ApiException(400, PRODUCT_NAME_ALREADY_EXISTS)

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

            product_thumbnail_id = seller_dao.create_product_thumbnail(product_info, connection)
            product_info['product_thumbnail_id'] = product_thumbnail_id
            seller_dao.create_product_thumbnail_log(product_info, connection)

            return product_id

        except ApiException as e:
            raise e
