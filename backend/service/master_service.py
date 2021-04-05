from model.master_dao   import MasterDao
from flask              import jsonify, json
from responses          import *

class MasterService:
  
  def account(self, connection, page_condition, filters):
    """ 샐러 계정 관리(마스터) - 리스트
      Author  
        : Sung joun Jang
      Args:
        # page_condition  
        limit           : 페이지당 보여질 데이터 갯수
        offset          : 현재 페이지
        # filters
        no              : 샐러의 no
        username        : 샐러 id
        english         : 브랜드의 영어 이름
        korean          : 브랜드의 한글 이름
        sellerType      : 샐러의 타입(일반, 헬피)
        sellerStatus    : 샐러의 상태(입점, 입점대기 등등)
        sellerAttribute : 샐러의 속성(쇼핑몰, 뷰티 등등)
        managerName     : 매니저의 이름
        managerPhone    : 매니저의 핸드폰 번호
        managerEmail    : 매니저의 이메일
        startDate       : 샐러 생성된 날짜의 시작 값
        endDate         : 샐러 생성된 날짜의 끝 값
      Returns 
        {
          "message": "SUCCESS",
          "result": [
            {
              "actions": [
                {
                  "id": 1,
                  "name": "입점 승인",
                  "sl.id": 2
                },
                {
                  "id": 2,
                  "name": "입점 거절",
                  "sl.id": 2
                }
            ],
              "attribute": "로드샵",
              "createdAt": "Fri, 03 Apr 2020 00:00:00 GMT",
              "english": "nanauhh",
              "korean": "우나나나",
              "managerEmail": "t2@gmail.com",
              "managerName": "담2",
              "managerPhone": "010-2",
              "no": 6,
              "sellerStatus": "입점 대기",
              "sellerType": "일반",
              "username": "nana"
            }
          ]
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
    master_dao = MasterDao()

    seller_type      = master_dao.seller_type(connection)
    seller_status    = master_dao.seller_status(connection)
    seller_attribute = master_dao.seller_attribute(connection)

    return {"data" : {
      "seller_type"      : seller_type,
      "seller_status"    : seller_status,
      "seller_attribute" : seller_attribute
    }}

  def account_level(self, connection, data):
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
    master_dao = MasterDao()

    categories =  master_dao.seller_category(connection)

    return {"data" : categories}

  def order_ready(self, connection, filters):
    master_dao = MasterDao()

    data        = master_dao.order_ready(connection, filters)
    order_count = master_dao.order_ready_count(connection, filters)
    total_count = order_count['COUNT(*)']

    return {"data" : data, "totalCount" : total_count}

  def order_ready_update(self, connection, data):
    master_dao = MasterDao()

    master_dao.order_ready_update(connection, data)
    master_dao.order_ready_update_log(connection, data)

    return {'custom_message':'updated', 'data':'PATCH'}
      