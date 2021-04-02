from flask  import json, jsonify
from model.seller_account_dao   import SellerDao
from responses                     import *

class SellerService:

    def seller_edit_get(self, user_id, connection):
        seller_dao = SellerDao()
        seller_get_service = seller_dao.seller_edit_get_dao(user_id, connection)
        seller_get_manager = seller_dao.get_seller_manager(user_id, connection)
        seller_get_service['managers'] = seller_get_manager

        return seller_get_service

    def seller_edit_service(self, user_id, seller_edit_info, connection):
        seller_dao = SellerDao()
        seller_edit_info['user_id'] = user_id
        
        # 새로 들어온 담당자 정보가 기존에 존재하는 정보인지 확인하는 과정
        if 'manager' in seller_edit_info:
            check_manager = seller_dao.check_seller_manager(seller_edit_info, connection)
            for check_one in check_manager:
                for one_input_manager in seller_edit_info:
                    if check_one['name'] == one_input_manager['name']:
                        raise (400, EXSISTING_MANAGER_NAME)
                    if check_one['email'] == one_input_manager['email']:
                        raise (400, EXSISTING_MANAGER_EMAIL)
                    if check_one['phone'] == one_input_manager['phone']:
                        raise (400, EXSISTING_MANAGER_PHONE)

        find_information = seller_dao.find_seller_info(user_id, connection)
        
        if None in find_information[0].values():
            if 'profile' not in seller_edit_info:
                raise ApiException(400, NOT_PROFILE)
            if 'introduce' not in seller_edit_info:
                raise ApiException(400, NOT_DESCRIPTION)
            if 'manager' not in seller_edit_info:
                raise ApiException(400, NOT_MANAGER)
            if 'callName' not in seller_edit_info:
                raise ApiException(400, NOT_CALL_NAME)
            if 'callStart' not in seller_edit_info:
                raise ApiException(400, NOT_CALL_START)
            if 'callEnd' not in seller_edit_info:
                raise ApiException(400, NOT_CALL_END)
            if 'postal_code' not in seller_edit_info:
                raise ApiException(400, NOT_POSTAL)
            if 'address' not in seller_edit_info:
                raise ApiException(400, NOT_ADDRESS)
            if 'detailAddress' not in seller_edit_info:
                raise ApiException(400, NOT_DETAIL_ADDRESS)
            if 'delivery_info' not in seller_edit_info:
                raise ApiException(400, NOT_SHIPPING_DESCRIPTION)
            if 'refund_info' not in seller_edit_info:
                raise ApiException(400, NOT_ORDER_DESCRIPTION)
            if 'manager' not in seller_edit_info:
                raise ApiException(400, NOT_MANAGER)

            # 추가정보인 셀러 상세소개의 길이가 10자 미만일 경우
            if 'description' in seller_edit_info:
                if len(seller_edit_info['description']) < 10:
                    raise ApiException(400, SHORT_INPUT_SELLER)
            # else:
            #     seller_edit_info['description'] = ""

            if 'backgroundImage' not in seller_edit_info:
                seller_edit_info['backgroundImage'] = None
            
            # 필수정보인 매니저의 상세 정보들중에 빈 값이 있을 경우
            if 'manager' in seller_edit_info:
                for one_manager in seller_edit_info['manager']:
                    if 'name' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_NAME)
                    if 'number' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_NUMBER)
                    if 'email' not in one_manager:
                        raise ApiException(400, NOT_MANAGER_EMAIL)
                    else:
                        managers = seller_edit_info['manager']
                        for row in managers:
                            one = {
                                'name'      : row['name'],
                                'email'     : row['email'],
                                'phone'     : row['phone'],
                                'user_id'   : user_id
                            }
                            seller_dao.update_information_manager(one, connection)

            # 고객센터의 주말 운영 여부가 체크되지 않아 값이 들어오지 않았을 경우 기본값인 0으로 지정
            if 'isWeekend' not in seller_edit_info:
                seller_edit_info['isWeekend'] = 0
            

            # 첫 내용 기입과 이력 생성
            seller_edit = seller_dao.seller_account_edit(seller_edit_info, connection)
            seller_dao.create_seller_update_log(user_id, connection)
            
            return seller_edit

        # 첫 수정페이지 작업 이후 필수값들이 모두 입력되어있는 상태에서 일부 값들만 수정할 경우
        else:
            # 수정내용에 manager 가 있을 경우
            if 'manager' in seller_edit_info:
                managers = seller_edit_info['manager']
                for row in managers:
                    one = {
                        'name'      : row['name'],
                        'email'     : row['email'],
                        'phone'     : row['phone'],
                        'user_id'   : user_id
                    }
                    # 다시 find 해서 id 같은 애 있으면 들어온 값으로 update 되도록 해야함
                    seller_dao.update_information_manager(one, connection)
            # 일부 수정과 이력 생성
            result = seller_dao.update_information(seller_edit_info, connection)
            create_log = seller_dao.create_seller_update_log(user_id, connection)
            return result
