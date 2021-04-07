from model.master_dao import MasterDao


class MasterService:

  def account(self, connection, filters):
    """ [어드민] 샐러 계정 관리(마스터)
      Author: 
        Sung joun Jang
      Args:    
        - limit: 페이지당 보여질 데이터 갯수
        - offset: 현재 페이지
        - no: 샐러의 no
        - username: 샐러 id
        - english: 브랜드의 영어 이름
        - korean: 브랜드의 한글 이름
        - sellerType: 샐러의 타입(일반, 헬피)
        - sellerStatus: 샐러의 상태(입점, 입점대기 등등)
        - sellerAttribute: 샐러의 속성(쇼핑몰, 뷰티 등등)
        - managerName: 매니저의 이름
        - managerPhone: 매니저의 핸드폰 번호
        - managerEmail: 매니저의 이메일
        - startDate: 샐러 생성된 날짜의 시작 값
        - endDate: 샐러 생성된 날짜의 끝 값
      Returns:
        message: 반환되는 메세지
        result: {
            data: 전달하는 데이터 값
            totalCount: 전체 데이터 개수
        }
    """

    master_dao = MasterDao()

    # 샐러 계정 리스트 반환
    account = master_dao.account(connection, filters)
    # totalCount 수 반환
    account_count = master_dao.account_count(connection, filters)
    total_count = account_count['totalCount']

    result = []
    action_map = {}
    for row in account:
      data = {
        'no': row['no'],
        'username': row['username'],
        'english': row['english'],
        'korean': row['korean'],
        'sellerType': row['seller_type'],
        'managerName': row['manager'],
        'sellerStatus': row['seller_status'],
        'managerPhone': row['phone'],
        'managerEmail': row['email'],
        'attribute': row['attribute'],
        'createdAt': row['created']
      }

      # 해당 샐러의 level에 따른 action 리스트를 반환
      if row['seller_status'] not in action_map:
        action_map[row['seller_status']] = master_dao.action(connection, row['seller_status'])

      data['actions'] = action_map[row['seller_status']]
      result.append(data)

    return {'data': result, 'totalCount': total_count}

  def account_init(self, connection):
    """ [어드민] 샐러 계정 관리(마스터) - 초기값
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        sellerType: 샐러의 타입 값
        sellerStatus: 샐러의 상태 값
        sellerAttribue: 샐러의 속성 값
    """
    master_dao = MasterDao()

    # 초기값에 필요한 타입들을 반환하는 로직
    seller_type = master_dao.seller_type(connection)
    seller_status = master_dao.seller_status(connection)
    seller_attribute = master_dao.seller_attribute(connection)

    return {'data': {
      'sellerType': seller_type,
      'sellerStatus': seller_status,
      'sellerAttribute': seller_attribute
    }}

  def account_level(self, connection, data):
    """ [어드민] 샐러 계정 관리(마스터) - level 값 변경하기
      Author: 
        Sung joun Jang
      Args:    
        - sellerId: 샐러의 pk 값
        - actionId: 액션의 pk 값
      Returns:
        custom_message: 개인화 메세지
        data: method 종류
    """
    master_dao = MasterDao()
    action_id = data['action_id']
    update_action = ''

    # 액션의 pk값을 name으로 반환하는 로직
    check_action = master_dao.check_action_id(connection, action_id)

    # 액션에 따른 레벨의 name 값을 매칭
    if check_action['name'] in ['입점 승인', '휴점 해제', '퇴점 철회 처리']:
      update_action = '입점'
    if check_action['name'] in ['입점 거절']:
      update_action = '입점 거절'
    if check_action['name'] in ['휴점 신청']:
      update_action = '휴점'
    if check_action['name'] in ['퇴점 신청처리']:
      update_action = '퇴점 대기'
    if check_action['name'] in ['퇴점 확정 처리']:
      update_action = '퇴점'
      # 퇴점일때 soft delete 실행
      master_dao.seller_delete(connection, data)

    # 레벨에 따른 name 값을 id로 변경
    update_level = master_dao.check_action_name(connection, update_action)
    data['update_level'] = update_level['id']

    # 해당 샐러의 레벨 값을 변경하는 함수(+ 내역 추가)
    master_dao.account_level(connection, data)
    master_dao.account_level_log(connection, data)

    return {'custom_message':'updated', 'data':'PATCH'}

  def order_ready_init(self, connection):
    """ [어드민] 주문관리(마스터) - 상품준비(초기값)
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        data: 전달하는 데이터 값
    """
    master_dao = MasterDao()

    # 초기값에 필요한 샐러 카테고리를 반환
    categories =  master_dao.seller_category(connection)

    return {'data': {
      'sellerAttribute': categories
    }}

  def order_ready(self, connection, filters):
    """ [어드민] 주문관리(마스터) - 상품준비(검색값)
      Author: 
        Sung joun Jang
      Args:    
        - filters: 필터에 대한 값들
        - page_condition: 페이지에 대한 값들
      Returns:
        data: 전달하는 데이터 값
        totalCount: 전체 데이터 개수
    """
    master_dao = MasterDao()

    # 주문 리스트를 반환
    data = master_dao.order_ready(connection, filters)
    # 주문 리스트의 count를 반환
    order_count = master_dao.order_ready_count(connection, filters)
    total_count = order_count['totalCount']

    return {'data': data, 'totalCount': total_count}

  def order_ready_update(self, connection, data):
    """ [어드민] 주문관리(마스터) - 상품준비(주문 상태 변경)
      Author: 
        Sung joun Jang
      Args:    

      Returns:
        custom_message: 개인화 메세지
        data: method 종류
    """
    master_dao = MasterDao()

    # 배송 상태를 배송중으로 변경(+ 내역 추가)
    master_dao.order_ready_update(connection, data)
    master_dao.order_ready_update_log(connection, data)

    return {'custom_message':'updated', 'data':'PATCH'}
  
  def order_detail(self, connection, cart_number):
    """ [어드민] 주문 상세 관리(마스터)
      Author: 
        Sung joun Jang
      Args:    
        - product_id: 조회하는 상품의 pk 값
        - cart_number: 조회하는 카트의 외부 고유 값
      Returns:
        orderDetails: 주문 상세의 필요한 값
        orderLogs: 해당 주문의 로그 값
    """
    master_dao = MasterDao()

    # 주문 상세를 반환
    order_detail = master_dao.order_detail(connection, cart_number)
    # 할인율을 없앤 원래의 가격
    order_detail['originalPrice'] = order_detail['unitOriginalPrice'] * order_detail['quantity']

    # 주문 상세에서 필요한 변경 이력의 데이터를 반환
    order_log = master_dao.order_detail_get_log(connection, cart_number)

    data = {
      'orderDetails': order_detail,
      'orderLogs': order_log
    }
    return {'data': data}
