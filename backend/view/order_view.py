from flask import request, Blueprint, jsonify, g
from db_connector import connect_db
from responses import *
from service.order_service import OrderService
from utils import login_decorator


class OrderView:
    order_app = Blueprint('order_app', __name__)

    @order_app.route('/cart', methods=['POST'])
    @login_decorator
    def post_cart():
        """ [서비스] 카트에 상품 담기
        Author:
            Mark Hasung Kim
        Returns:
            {
                    "custom_message": "SUCCESS",
                    "result": "POST
                    }
        """
        connection = None
        try:
            data = request.json
            user_id = g.token_info['user_id']
            products = data['products']

            if 'products' not in data:
                raise ApiException(400, INVALID_INPUT)
            if 'productId' not in data:
                raise ApiException(400, INVALID_INPUT)
            if not products:
                raise ApiException(400, INVALID_INPUT)
            for product in products:
                if 'color' not in product:
                    raise ApiException(400, COLOR_NOT_IN_INPUT)
                if 'size' not in product:
                    raise ApiException(400, SIZE_NOT_IN_INPUT)
                if 'quantity' not in product:
                    raise ApiException(400, QUANTITY_NOT_IN_INPUT)
                if 'price' not in product:
                    raise ApiException(400, PRICE_NOT_IN_INPUT)

            order_info = {
                'user_id': user_id,
                'product_id': data['productId']
            }

            connection = connect_db()
            order_service = OrderService()
            order_service.post_cart(order_info, products, connection)
            connection.commit()

            return {"custom_message": "SUCCESS", "result": "POST"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @order_app.route('/cart', methods=['GET'])
    @login_decorator
    def get_cart():
        """ [서비스] 유저의 모든 카트들을 가져오기
        Author:
            Mark Hasung Kim
        Returns:
            cart_details (유저의 모든 카트 정보)
        """
        connection = None
        try:
            user_id = g.token_info['user_id']
            order_info = {'user_id': user_id}
            connection = connect_db()
            order_service = OrderService()
            cart_details = order_service.get_cart(order_info, connection)

            return cart_details

        except Exception as e:
            raise e
        finally:
            if connection:
                connection.close()

    @order_app.route('/cart', methods=['DELETE'])
    @login_decorator
    def delete_cart():
        """ [서비스] 카트 삭제 하기 (is_delete = 1)
        Author:
            Mark Hasung Kim
        Returns:
            {
                    "custom_message": "SUCCESS",
                    "result": "DELETE"
                    }
        """
        user_id = g.token_info['user_id']
        connection = None
        try:
            data = request.json
            if 'productOptionIds' not in data:
                raise ApiException(400, PRODUCT_OPTION_NOT_IN_INPUT)

            order_info = {
                'user_id': user_id,
                'product_option_ids': data['productOptionIds']
            }

            connection = connect_db()
            order_service = OrderService()
            order_service.delete_cart(order_info, connection)
            connection.commit()

            return {'custom_message': 'SUCCESS', 'result': 'DELETE'}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    
    @order_app.route('/shipping-memo', methods=['GET'])
    def get_shipping_memo():

        """[서비스] user가 주문시 배송메모 선택하는 드롭박스
        Author:
            Ji Yoon Lee
        Returns:
            - 200:
                { "message"   : "SUCCESS"
                    "result"    : {
                        "data" : 배송 메모 리스트
                    }
                }
            - 400: 요청 실패시 "요청에 실패하였습니다"
        """

        connection = None
        try:
            connection = connect_db()

            if connection:
                order_service = OrderService()
                memo_option  = order_service.get_shipping_memo(connection)

                return memo_option

        except Exception as e:
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()


    @order_app.route('/address', methods=['GET'])
    @login_decorator
    def get_address():

        """[서비스] user가 주문시 이전 배송지 존재하면 가져오기
        Author:
            Ji Yoon Lee
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200:
                { "message"   : "SUCCESS"
                    "result"    : {
                        "data" : 배송지 목록
                    }
                }
            - 400: 요청 실패시 "요청에 실패하였습니다"
        """

        connection = None
        try:
            user_id    = g.token_info["user_id"]
            connection = connect_db()

            if connection:
                order_service = OrderService()
                address_option  = order_service.get_address(user_id, connection)

                return address_option

        except Exception as e:
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()

    @order_app.route('/address/add', methods=['POST'])
    @login_decorator
    def post_address():

        """ [서비스] user가 주문시 새로운 배송지 추가
        Author:
            Ji Yoon Lee
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
            - body(dict) : "name", "phone", "postal", "address", "addressDetail", "isDefault"(optional)
        Returns:
            - 200 :  
                { "message"   : "SUCCESS"
                    "result"    : {
                        "data" : 새로 등록된 주소 id (address_id)
                    }
                }
            - 400 : 필수 parameter 미입력시 "** 정보를 입력해 주세요"
        
        Note:
            - 배송지의 address, address_detail이 동일한 주소는 중복 등록 불가
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
            
            if "addressDetail" not in data:
                raise ApiException(400, "상세주소를 입력해주세요")

            address_info = {
                "user_id"                  : g.token_info["user_id"],
                "recipient_name"           : data["name"],
                "recipient_phone"          : data["phone"],
                "recipient_postal_code"    : data["postal"],
                "recipient_address"        : data["address"],
                "recipient_address_detail" : data["addressDetail"],
                "is_default"               : data.get("isDefault", 0)
            }

            connection = connect_db()

            if connection:
                order_service = OrderService()
                post_address  = order_service.post_address(address_info, connection)
                connection.commit()

                return post_address

        except Apiexception as e:
            connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @order_app.route('/address/delete', methods=['DELETE'])
    @login_decorator
    def delete_address():

        """ [서비스] user가 주문시 기존 배송지 삭제
        Author:
            Ji Yoon Lee
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
            - body(dict) : 삭제할 주소의 "addressId"
        Returns:
            - 200 :  
                { "message"   : "SUCCESS"
                    "result"    : {
                        "data" : 삭제된 주소 id (address_id)
                    }
                }
            - 400 : 필수 parameter 미입력시 "** 정보를 입력해 주세요"
        """

        connection = None
        try:
            data = request.json

            if "addressId" not in data:
                raise ApiException(400, SELECT_ADDRESS_TO_DELETE)

            address_info = {
                "user_id"    : g.token_info["user_id"],
                "address_id" : data["addressId"]
            }

            connection = connect_db()

            if connection:
                order_service = OrderService()
                address_id  = order_service.delete_address(address_info, connection)
                connection.commit()

                return address_id

        except Exception as e:
            connection.rollback()
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()



    @order_app.route('/direct-purchase', methods=['POST'])
    @login_decorator
    def post_order_confirmation_direct():

        """ [서비스] 제품 상세페이지에서 바로결제로 주문 (배송정보 입력페이지로 넘어가는 부분)
        Author:
            Ji Yoon Lee
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
            - body(dict) : 바로결제 할 상품의 "productId"
        Returns:
            - 200 :  
                { "message"   : "SUCCESS"
                    "result"    : {
                        "data" : 주문 id (orderId)
                    }
                }
            - 400 : 필수 parameter 미입력시 "** 정보를 입력해 주세요"
        """

        connection = None
        try:
            data = request.json
            products = data["products"] 

            if "productId" not in data:
                raise ApiException(400, PRODUCT_MISSING)

            order_info = {
                "user_id" : g.token_info["user_id"],
                "product_id" : data["productId"],
                "order_status_type_id" : 3,
            }

            connection = connect_db()

            if connection:
                order_service = OrderService()
                order_id  = order_service.direct_purchase(order_info, products, connection) 
                connection.commit()

                return order_id

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()


    @order_app.route('/confirmation', methods=['PATCH'])
    @login_decorator
    def post_order_confirmation():

        """ [서비스] 결제페이지 (배송정보 입력 후 결제 버튼 누른 다음)
        Author:
            Ji Yoon Lee
        Args:
            - token(str) : 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
            - body(dict) : "name", "phone", "postal", "address", "addressDetail", "isDefault"(optional)
        Returns:
            - 200 :  
                { "message"   : "SUCCESS"
                    "result"    : {
                        "data" : 새로 등록된 주소 id (address_id)
                    }
                }
            - 400 : 필수 parameter 미입력시 "** 정보를 입력해 주세요"
        
        Note:
            - 배송지의 address, address_detail이 동일한 주소는 중복 등록 불가
        """

        """
        주문결제 post (장바구니 다음단계 페이지)
        """

        connection = None
        try:
            data = request.json

            if "orderName" not in data:
                raise ApiException(400, "주문자 이름을 입력해주세요")

            if "orderPhone" not in data:
                raise ApiException(400, "주문자 전화번호를 입력해주세요")
            
            if "orderEmail" not in data:
                raise ApiException(400, "주문자 이메일을 입력해주세요")

            if "items" not in data:
                raise ApiException(400, "주문할 상품이 없습니다")

            order_info = {
                "order_id" : data["orderId"],
                "user_id" : g.token_info["user_id"],
                "order_name" : data["orderName"],
                "order_phone" : data["orderPhone"],
                "order_email" : data["orderEmail"],
                "shipping_memo_type_id" : data.get("shippingMemoTypeId"),
                "shipping_info_id" : data["shippingInfoId"],
                "items" : data["items"],
                "total_price" : data["totalPrice"]
            }

            connection = connect_db()

            if connection:
                order_service = OrderService()
                order_confirm  = order_service.order_confirm(order_info, connection)
                connection.commit()

                return order_confirm

        except Exception as e:
            connection.rollback()
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()


    
