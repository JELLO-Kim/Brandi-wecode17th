from model.master_dao   import MasterDao
from flask              import jsonify, json
from responses          import *

class MasterService:
  
  def account(self, connection, page_condition):
    master_dao  = MasterDao()
    account     = master_dao.account(connection, page_condition)
    # totalCount 수 반환
    account_count = master_dao.account_count(connection)
    # total_count   = account_count['COUNT(*)']

    result = [{
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
    } for row in account]

    return {"data" : result}
    # return {"data" : result, "totalCount" : total_count}