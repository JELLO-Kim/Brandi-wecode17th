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
    update_action = 0

    # 똑같은 이름이면 해당 dao로 보내서 해당하는 id 값들만 받아올 수 있을듯!    
    if action_id in [1, 5, 9]:
      update_action = 3
    if action_id in [2]:
      update_action = 4
    if action_id in [3, 11]:
      update_action = 6
    if action_id in [4, 6]:
      update_action = 7
    if action_id in [8]:
      update_action = 8
      master_dao.seller_delete(connection, data)

    data['update_action']

    return master_dao.account_level(connection, data)