from model.master_dao   import MasterDao
from flask              import jsonify, json
from responses          import *

class MasterService:
  
  def account(self, connection, page_condition, filters):
    master_dao = MasterDao()

    account     = master_dao.account(connection, page_condition, filters)
    # totalCount 수 반환
    account_count = master_dao.account_count(connection, filters)
    total_count   = account_count['COUNT(*)']

    # result = [{
    #   'no'           : row['no'],
    #   'username'     : row['username'],
    #   'english'      : row['english'],
    #   'korean'       : row['korean'],
    #   'sellerType'   : row['seller_type'],
    #   'managerName'  : row['manager'],
    #   'sellerStatus' : row['seller_status'],
    #   'managerPhone' : row['phone'],
    #   'managerEmail' : row['email'],
    #   'attribute'    : row['attribute'],
    #   'createdAt'    : row['created']
    # } for row in account]

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
    # update_action = ""

    # check_action = master_dao.check_action_id(connection, action_id)

    # if check_action in ["입점 승인", "휴점 해제", "퇴점 철회 처리"]:
    #   update_action = "입점"
    # if check_action in ["입점 거절"]:
    #   update_action = "입점 거절"
    # if check_action in ["휴점 신청"]:
    #   update_action = "휴점"
    # if check_action in ["퇴점 신청처리"]:
    #   update_action = "퇴점 대기"
    # if check_action in ["퇴점 확정 처리"]:
    #   update_action = "퇴점"
    #   master_dao.seller_delete(connection, data)

    # data['update_level'] = master_dao.check_action_name(connection, update_action)
    master_dao.account_level(connection, data)

    return {'custom_message':'updated', 'result':'PATCH'}