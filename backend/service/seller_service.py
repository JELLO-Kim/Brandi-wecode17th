import bcrypt
import jwt
from flask import jsonify
from model.seller_dao import SellerDao
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

<<<<<<< HEAD
        if seller['user_type_id'] != 2:
            raise ApiException(403, IS_NOT_SELLER)
=======
        if seller['user_type_id'] not in [2, 3]:
            raise ApiException(400, IS_NOT_SELLER)
>>>>>>> b17f311... [어드민] seller 상세정보 수정

        if seller:
            if bcrypt.checkpw(seller_login_info['password'].encode('utf-8'), seller['password'].encode('utf-8')):
                token = jwt.encode({'user_id': seller['id']}, SECRET_KEY, ALGORITHM)
                user_id = seller['id']
<<<<<<< HEAD
                return jsonify({'accessToken': token, 'userId': user_id}), 201
=======
                user_type_id = seller['user_type_id']
                return jsonify({'accessToken': token, 'userId': user_id, "userTypeId" : user_type_id}), 201
>>>>>>> b17f311... [어드민] seller 상세정보 수정

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

<<<<<<< HEAD
    def seller_edit_get(self, user_id, connection):
        """ [어드민] seller의 본인 상세 정보수정 페이지 입장 시 확인되는 정보
=======
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

        # 로그인한 seller의 추가정보 내용 확인 (첫번째 수정이라면 회원가입시 입력했던 정보 외에 null과 빈 string으로 처리되어 있음)
        find_information = seller_dao.find_seller_info(user, connection)
        # 필수입력 정보중 None이 있다면 첫 수정으로 간주. 필수 parameter들이 요구된다.
        if None in find_information.values():
            SellerService().first_update(user, seller_edit_info, connection)
        else:
            SellerService().seconde_update(user, seller_edit_info, connection)

    def first_update(self, user, seller_edit_info, connection):
        """ [어드민] seller의 본인 상세 정보 수정 : 회원가입 후 첫 수정
>>>>>>> b17f311... [어드민] seller 상세정보 수정
        Author : Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
<<<<<<< HEAD
        Returns
            : seller의 상세 정보 반환
        Note
            : n개로 존재할 수 있는 manager에 대한 정보들은 manager라는 key값 안에 존재
        """
        seller_dao = SellerDao()
        seller_get_service = seller_dao.seller_edit_get_dao(user_id, connection)
        seller_get_manager = seller_dao.get_seller_manager(user_id, connection)
        seller_get_service['managers'] = seller_get_manager

        return seller_get_service

    def seller_edit_service(self, user_id, seller_edit_info, connection):
        """ [어드민] seller의 본인 상세 정보수정 페이지 입장 시 확인되는 정보
=======
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
        if not seller_edit_info['manager']:
            raise ApiException(400, NOT_MANAGER)
        if not seller_edit_info['delivery_info']:
            raise ApiException(400, NOT_SHIPPING_DESCRIPTION)
        if not seller_edit_info['refund_info']:
            raise ApiException(400, NOT_ORDER_DESCRIPTION)

        # 선택 추가사항인 셀러의 상세소개에 대한 값이 들어왔지만 길이가 10자 미만일 경우
        if seller_edit_info['description']:
            if len(seller_edit_info['description']) < 10:
                raise ApiException(400, SHORT_INPUT_SELLER)

        # 필수정보인 매니저의 상세 정보들중에 빈 값이 있을 경우
        for one_manager in seller_edit_info['manager']:
            if 'name' not in one_manager:
                raise ApiException(400, NOT_MANAGER_NAME)
            if 'phoneNumber' not in one_manager:
                raise ApiException(400, NOT_MANAGER_NUMBER)
            if 'email' not in one_manager:
                raise ApiException(400, NOT_MANAGER_EMAIL)
            else:
                one = {
                    'name'      : one_manager['name'],
                    'email'     : one_manager['email'],
                    'phoneNumber'     : one_manager['phoneNumber'],
                    'user_id'   : seller_edit_info['user_id']
                }
                result = seller_dao.insert_information_manager(one, connection)
                extra = {
                    'changeId' : result,
                    'user_id' : seller_edit_info['user_id']
                }
                seller_dao.create_manager_log(result, extra, connection)
        # 첫 내용 기입과 이력 생성
        seller_edit = seller_dao.update_information(seller_edit_info, connection)
        seller_dao.create_seller_update_log(seller_edit_info, connection)


        return True

        # 첫 수정페이지 작업 이후 필수값들이 모두 입력되어있는 상태에서 일부 값들만 수정할 경우
        
    def seconde_update(self, user, seller_edit_info, connection):
        """ [어드민] seller의 본인 상세 정보 수정 : 필수정보 입력 후 두번째 수정(일부 내역만 수정 가능)
>>>>>>> b17f311... [어드민] seller 상세정보 수정
        Author : Chae hyun Kim
        Args:
            connection : 커넥션
            user_id : 로그인 유저의 user_id
<<<<<<< HEAD
            seller_edit_info : 새로 입력될 내용들 (dict 형태)
        Returns
            : 수정된 정보의 갯수 반환
        Note
            1. 회원가입 후 첫 수정 : 필수입력란이 null 이면 모든 값을 다 입력하도록 함 / 빠진 정보가 있다면 적절한 error 반환
            2. 필수입력란 작성 후 개별 수정 : 수정을 원하는 값에 한하여 새로 입력되도록 함
            3. manager는 한번에 여러개의 정보를 입력할 수 있도록 "배열"로 받은 뒤 for loop 진행
        """
        seller_dao = SellerDao()

        # 새로 들어온 담당자 정보가 기존에 존재하는 정보인지 확인하는 과정 (id가 같은데 입력된 정보가 다를 경우)
        if seller_edit_info['manager'] != None:
            check_manager = seller_dao.check_seller_manager(seller_edit_info, connection)
            for check_one in check_manager:
                for one_input_manager in seller_edit_info['manager']:
                    if check_one['name'] == one_input_manager['name']:
                        raise ApiException(400, EXSISTING_MANAGER_NAME)
                    if check_one['email'] == one_input_manager['email']:
                        raise ApiException(400, EXSISTING_MANAGER_EMAIL)
                    # if check_one['phone'] == one_input_manager['phone_number']:
                    #     raise (400, EXSISTING_MANAGER_PHONE)

        # 로그인한 seller의 추가정보 내용 확인 (첫번째 수정이라면 회원가입시 입력했던 정보 외에 null로 처리되어 있음)
        find_information = seller_dao.find_seller_info(user_id, connection)

        # 필수입력 정보중 None이 있다면 첫 수정으로 간주. 필수 parameter들이 요구된다.
        if None in find_information[0].values():
            print('??????????', seller_edit_info)
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
            if not seller_edit_info['manager']:
                raise ApiException(400, NOT_MANAGER)

            # 선택 추가사항인 새로 입력될 셀러 상세소개의 길이가 10자 미만일 경우
            if 'description' in seller_edit_info:
                if len(seller_edit_info['description']) < 10:
                    raise ApiException(400, SHORT_INPUT_SELLER)

            # 필수정보인 매니저의 상세 정보들중에 빈 값이 있을 경우
            if seller_edit_info['manager']:
                for one_manager in seller_edit_info['manager']:
                    if 'name' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_NAME)
                    if 'phone' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_NUMBER)
                    if 'email' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_EMAIL)
                    else:
                        managers = seller_edit_info['manager']
                        for row in managers:
                            one = {
                                'name': row['name'],
                                'email': row['email'],
                                'phone': row['phone'],
                                'user_id': seller_edit_info['user_id']
                            }
                            seller_dao.insert_information_manager(one, connection)

            # 고객센터의 주말 운영 여부가 체크되지 않아 값이 들어오지 않았을 경우 기본값인 0으로 지정
            if 'isWeekend' not in seller_edit_info:
                seller_edit_info['isWeekend'] = 0

            # 첫 내용 기입과 이력 생성
            seller_edit = seller_dao.update_information(seller_edit_info, connection)
            seller_dao.create_seller_update_log(seller_edit_info, connection)

            return seller_edit

        # 첫 수정페이지 작업 이후 필수값들이 모두 입력되어있는 상태에서 일부 값들만 수정할 경우
        else:
            # 수정내용에 manager 가 있을 경우 배열로 처리된 것을 for loop을 통해 한명의 매니저에 대한 내용 반복적으로 생성
            if seller_edit_info['manager']:
                for one_manager in seller_edit_info['manager']:
                    if 'name' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_NAME)
                    if 'phone' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_NUMBER)
                    if 'email' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_EMAIL)
                managers = seller_edit_info['manager']
                # body에 담겨져 들어온 manager에 대한 정보가 신규정보가 아닌 기존 정보의 수정일 경우 update 진행
                check_manager = seller_dao.check_seller_manager(seller_edit_info, connection)
                for row in managers:
                    for check_one in check_manager:
                        one = {
                            'id': row.get('id', None),
                            'name': row.get('name', None),
                            'email': row.get('email', None),
                            'phone': row.get('phone', None),
                            'user_id': user_id
                        }
                        if check_one['id'] == one['id']:
                            seller_dao.update_manager(one, connection)
                        # 작성된 manager와 같은 id 값이 아닐 경우 매니저 신규 생성
                    print('one은 이거==========', one)
                    seller_dao.insert_information_manager(one, connection)
            # 일부 수정과 이력 생성
            # result = seller_dao.update_information(seller_edit_info, connection)
            # create_log = seller_dao.create_seller_update_log(user_id, connection)
            print('return 직전입니당!!!!!!!!!!!!!!!!!!!')
            return "okokok"

=======
            seller_edit_info : 새로 입력될 내용들
        Returns
            : True
        Note:
            1. 삭제되어있지 않은 manager가 이미 3명이라면 error message 반환
            2. 기존에 입력된 manager에 대한 정보 수정일 경우 insert가 아닌 update 진행
            3. manager는 한번에 여러개의 정보를 입력할 수 있도록 "배열"로 받은 뒤 for loop 진행
        """
        seller_dao = SellerDao()
        # 수정내용에 manager 가 있을 경우 배열로 처리된 것을 for loop을 통해 한명의 매니저에 대한 내용 반복적으로 생성
        # 먼저 name, phone, email 키값이 다 들어왔는지 확인하기
        if seller_edit_info['managers']:
            for one_manager in seller_edit_info['managers']:
                if 'name' not in one_manager:
                    raise ApiException(400, NOT_MANAGER_NAME)
                if 'phoneNumber' not in one_manager:
                    raise ApiException(400, NOT_MANAGER_NUMBER)
                if 'email' not in one_manager:
                    raise ApiException(400, NOT_MANAGER_EMAIL)

            # body에 담겨져 들어온 manager에 대한 정보가 신규정보가 아닌 기존 정보의 수정일 경우 update 진행 + 이력 생성
            for row in seller_edit_info['managers']:
                check_manager_num = seller_dao.check_seller_manager_number(user, connection)
                if check_manager_num['COUNT(*)'] >3:
                    raise ApiException(400, MAXIMUN_MANAGER)
                check_manager = seller_dao.get_seller_manager(user, connection)
                one = {
                    'id': row.get('id', None),
                    'name': row.get('name', None),
                    'email': row.get('email', None),
                    'phoneNumber': row.get('phoneNumber', None),
                    'user_id': user['user_id']
                }
                for check_one in check_manager:
                    if check_one['id'] == one['id']:
                        seller_dao.update_manager(one, connection)
                        extra = {
                            'changeId' : one['id'],
                            'user_id' : seller_edit_info['user_id']
                        }
                        seller_dao.create_manager_log(extra, connection)
                    else:
                        if check_one['email'] == one['email']:
                            raise ApiException(400, EXSISTING_MANAGER_EMAIL)
                        if check_one['phoneNumber'] == one['phoneNumber']:
                            raise (400, EXSISTING_MANAGER_PHONE)
                            
                    # 작성된 manager와 같은 id 값이 아닐 경우 매니저 신규 생성&이력 생성
                if one['id'] is None:
                    result = seller_dao.insert_information_manager(one, connection)
                    extra = {
                        'changeId' : result,
                        'user_id' : seller_edit_info['user_id']
                    }
                    seller_dao.create_manager_log(extra, connection)
        # 그 외의 정보에 대해 일부 수정과 이력 생성
        else:
            seller_dao.update_information(seller_edit_info, connection)
            seller_dao.create_seller_update_log(user, connection)
        return True



# 채현 : delete
    def seller_edit_delete(self, man_id, connection):
        try:
            seller_dao = SellerDao()
            seller_dao.delete_manager_dao(man_id, connection)
        except ApiException as e:
            raise e

# 하성님 코드
>>>>>>> b17f311... [어드민] seller 상세정보 수정
    def post_product(self, product_info, product_options, connection):
        try:
            seller_dao = SellerDao()
            product_name_exists = seller_dao.check_existing_product_name(product_info, connection)

            if product_name_exists:
                raise ApiException(400, PRODUCT_NAME_ALREADY_EXISTS)

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

        except ApiException as e:
            raise e
