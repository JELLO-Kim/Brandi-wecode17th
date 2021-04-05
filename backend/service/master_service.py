from model.master_dao   import MasterDao
from flask              import jsonify, json
from responses          import *

class MasterService:
  
  def account(self, connection, page_condition, filters):
    """ [어드민] 샐러 계정 관리(마스터)
      Author: 
        Sung joun Jang
      Args:    
        - limit           : 페이지당 보여질 데이터 갯수
        - offset          : 현재 페이지
        - no              : 샐러의 no
        - username        : 샐러 id
        - english         : 브랜드의 영어 이름
        - korean          : 브랜드의 한글 이름
        - sellerType      : 샐러의 타입(일반, 헬피)
        - sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
        - sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
        - managerName     : 매니저의 이름
        - managerPhone    : 매니저의 핸드폰 번호
        - managerEmail    : 매니저의 이메일
        - startDate       : 샐러 생성된 날짜의 시작 값
        - endDate         : 샐러 생성된 날짜의 끝 값
      Returns:
        message : 반환되는 메세지
        result  : {
            data : 전달하는 데이터 값
            totalCount : 전체 데이터 개수
        }
    """

    master_dao = MasterDao()

    account     = master_dao.account(connection, page_condition, filters)
    # totalCount 수 반환
    account_count = master_dao.account_count(connection, filters)
    total_count   = account_count['COUNT(*)']

    result = []
    for row in account:
      data = {
        'no'           : row['no'],
        'username'     : row['username'],
        'english'      : row['english'],
        'korean'       : row['korean'],
        'sellerType'   : row['seller_type'],
        'managerName'  : row['manager'],
        'sellerStatus' : row['seller_status'],
        'managerPhone' : row['phone'],
        'managerEmail' : row['email'],
        'attribute'    : row['attribute'],
        'createdAt'    : row['created']
      }

      data['actions'] = master_dao.action(connection, row['seller_status'])
      result.append(data)

    return {"data" : result, "totalCount" : total_count}

  def account_init(self, connection):
    """ [어드민] 샐러 계정 관리(마스터) - 초기값
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        sellerType : 샐러의 타입 값
        sellerStatus : 샐러의 상태 값
        sellerAttribue : 샐러의 속성 값
    """
    master_dao = MasterDao()

    seller_type      = master_dao.seller_type(connection)
    seller_status    = master_dao.seller_status(connection)
    seller_attribute = master_dao.seller_attribute(connection)

    return {"data" : {
      "sellerType"      : seller_type,
      "sellerStatus"    : seller_status,
      "sellerAttribute" : seller_attribute
    }}

  def account_level(self, connection, data):
    """ [어드민] 샐러 계정 관리(마스터) - level 값 변경하기
      Author: 
        Sung joun Jang
      Args:    
        - sellerId : 샐러의 pk 값
        - actionId : 액션의 pk 값
      Returns:
        custom_message : 개인화 메세지
        data : method 종류
    """
    master_dao    = MasterDao()
    action_id     = data['action_id']
    update_action = ""

    check_action = master_dao.check_action_id(connection, action_id)

    if check_action['name'] in ["입점 승인", "휴점 해제", "퇴점 철회 처리"]:
      update_action = "입점"
    if check_action['name'] in ["입점 거절"]:
      update_action = "입점 거절"
    if check_action['name'] in ["휴점 신청"]:
      update_action = "휴점"
    if check_action['name'] in ["퇴점 신청처리"]:
      update_action = "퇴점 대기"
    if check_action['name'] in ["퇴점 확정 처리"]:
      update_action = "퇴점"
      master_dao.seller_delete(connection, data)

    update_level = master_dao.check_action_name(connection, update_action)
    data['update_level'] = update_level['id']

    master_dao.account_level(connection, data)
    master_dao.account_level_log(connection, data)

    return {'custom_message':'updated', 'data':'PATCH'}

  def order_ready_init(self, connection):
    """ [어드민] 주문관리(마스터) - 상품준비(초기값)
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        data : 전달하는 데이터 값
    """
    master_dao = MasterDao()

    categories =  master_dao.seller_category(connection)

    return {"data" : {
      "sellerAttribute" : categories
    }}

  def order_ready(self, connection, filters):
    """ [어드민] 주문관리(마스터) - 상품준비(검색값)
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        data : 전달하는 데이터 값
        totalCount : 전체 데이터 개수
    """
    master_dao = MasterDao()

    data        = master_dao.order_ready(connection, filters)
    order_count = master_dao.order_ready_count(connection, filters)
    total_count = order_count['COUNT(*)']

    return {"data" : data, "totalCount" : total_count}

  def order_ready_update(self, connection, data):
    """ [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경)
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        custom_message : 개인화 메세지
        data : method 종류
    """
    master_dao = MasterDao()

    master_dao.order_ready_update(connection, data)
    master_dao.order_ready_update_log(connection, data)

    return {'custom_message':'updated', 'data':'PATCH'}
  
  def order_detail(self, connection, product_id, cart_number):
    """ [어드민] 주문 상세 관리(마스터)
      Author: 
        Sung joun Jang
      Args:    
        - product_id : 조회하는 상품의 pk 값
        - cart_number : 조회하는 카트의 외부 고유 값
      Returns:
        orderDetails : 주문 상세의 필요한 값
        orderLogs : 해당 주문의 로그 값
    """
    master_dao = MasterDao()

    order_detail = master_dao.order_detail(connection, product_id, cart_number)
    order_detail['originalPrice'] = order_detail['unitOriginalPrice'] * order_detail['quantity']

    order_log = master_dao.order_detail_log(connection, cart_number)

    data = {
      'orderDetails' : order_detail,
      'orderLogs'    : order_log
    }
    return {'data': data}