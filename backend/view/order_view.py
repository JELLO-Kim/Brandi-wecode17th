from flask          import request, Blueprint, jsonify
from db_connector   import connect_db
from service        import OrderService 
from responses      import *

class OrderView:
    order_app = Blueprint('order_app', __name__, url_prefix='/orders')

    @login_decorator
    @order_app.route('/address', methods=['GET'])
    def get_address():

        """ 
        order page의 배송지 변경시 뜨는 모달 창에 보여질 값 
        """

        connection = None
        try:
            user_id    = g.token_info["user_id"]
            connection = connect_db()

            if connection:
                order_service = OrderService()
                address_option  = order_service.get_address_option(user_id, connection)

                return address_option

        except Exception as e:
            raise ApiException(400, PAGE_NOT_FOUND)

        finally:
            if connection:
                connection.close()


    @login_decorator
    @order_app.route('/address/add', methods=['POST'])
    def post_address():
        """
        주문시 기존 배송지 외 신규배송지 추가
        """

        connection = None
        try:
            data = request.json

            if "name" not in data:
                raise ApiException(400, "이름을 입력해주세요")
            
            if "phone" not in data:
                raise ApiException(400, "전화번호를 입력해주세요")

            if "postal" not in data:
                raise ApiException(400, "우편번호를 입력해주세요")
            
            if "address" not in data:
                raise ApiException(400, "주소를 입력해주세요")
            
            if "address_detail" not in data:
                raise ApiException(400, "상세주소를 입력해주세요") 

            address_info = {
                "user_id"                  : g.token_info["user_id"],
                "recipient_name"           : data["name"],
                "recipient_phone"          : data["phone"],
                "recipient_postal_code"    : data["postal"],
                "recipient_address"        : data["address"],
                "recipient_address_detail" : data["address_detail"],
                "is_default"                : data["isDefault"]
            }

            connection = connect_db()

            if connection:
                order_service = OrderService()
                post_address  = order_service.post_address(address_info, connection)

                return psot_address

        except Exception as e:
            raise ApiException(400, PAGE_NOT_FOUND)

        finally:
            if connection:
                connection.close()





    @login_decorator
    @order_app.route('/confirmation', methods=['PATCH'])
    def post_order_confirmation():

        """
        주문결제 post (장바구니 다음단계 페이지)
        """

        connection = None
        try:
            data       = request.json

            if "orderName" not in data:
                raise ApiException(400, "주문자 이름을 입력해주세요")

            if "orderPhone" not in data:
                raise ApiException(400, "주문자 전화번호를 입력해주세요")
            
            if "orderEmail" not in data:
                raise ApiException(400, "주문자 이메일을 입력해주세요")

            if "items" not in data:
                raise ApiException(400, "주문할 상품이 없습니다")
                
            order_info = {
                "user_id" : g.token_info["user_id"],
                "order_name" : data["orderName"],
                "order_phone" : data["orderPhone"],
                "order_email" : data["orderEmail"],
                "shipping_memo_id" : data.get("shippingMemoId"),
                "shipping_info_id" : data["shippingInfoId"],
                "total_price" : data["totalPrice"],
                "items" : data["item"]
            }

            """
            items: 결제할 상품들의 cart id의 리스트
            """

            connection = connect_db()

            if connection:
                order_service = OrderService()
                order_confirm  = order_service.post_order_confirm(order_info, connection)

                return order_confirm

        except Exception as e:
            raise ApiException(400, PAGE_NOT_FOUND)

        finally:
            if connection:
                connection.close()