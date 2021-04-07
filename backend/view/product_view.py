from flask import request, Blueprint, g
from db_connector import connect_db
from service import ProductService
from responses import *
from config import AWS_ID, AWS_KEY


class ProductView:
    product_app = Blueprint('product_app', __name__, url_prefix='/products')

    @product_app.route('/category', methods=['GET'])
    def products_category():
        """ 상품 카테고리 list
        Author:  
            Chae hyun Kim
        Returns: 
            - 200: { "message"   : "SUCCESS"
                     "result"    : {
                        "data"       : category_list,
                        "totalCount" : 2차 카테고리 총 갯수
                        }
                    }
        """
        connection = None
        try:
            connection = connect_db()
            produts_category_service = ProductService()
            category_list = produts_category_service.products_category(connection)

            return category_list

        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection:
                connection.close()

    # products list에 대한 로직
    @product_app.route('/list', methods=['GET'])
    def products_list():
        """ products list
        Author:  
            Chae hyun Kim
        Args:    
            - query parameter : 필요할 경우 category의 id, limit과 offset 조건을 query paramter로 받는다
        Returns: 
            - 200: { 
                        "message" : "SUCCESS",
                        "result"  : {
                            "data" : product list,
                            "totalCount" : 상품 총 갯수
                        }
                    }
        Note:    
            - filtering 조건으로 category의 id가 query parameter를 통해 들어올 경우 해당 조건에 해당하는 product list로 결과 반환
        """
        MINIMUM_CATEGORY_NUMBER = 4
        MAXIMUM_CATEGORY_NUMBER = 5
        connection = None
        try:
            connection = connect_db()
            products_service = ProductService()
            page_condition = {}
            category    = request.args.get('category', None)
            limit       = request.args.get('limit', None)
            offset      = request.args.get('offset', None)

            # filtering 조건으로 들어올 category의 값이 허용 범위를 넘었을 경우 에러 반환
            if category is not None:
                if int(category) < MINIMUM_CATEGORY_NUMBER or int(category) > MAXIMUM_CATEGORY_NUMBER :
                    raise ApiException(404, INVALID_FILTER_CONDITION)
                page_condition['category'] = category

            # "더보기"를 누르기 전 limit 조건이 들어오지 않았을 경우 기본으로 30으로 지정
            if limit is None:
                page_condition['limit'] = 30
            else:
                page_condition['limit'] = int(limit)

            # "더보기"를 누르기 전 offset 조건이 들어오지 않았을 경우 기본으로 0으로 지정
            if offset is None:
                page_condition['offset'] = 0
            else:
                page_condition['offset'] = int(offset)

            product_list = products_service.products_list(connection, page_condition)

            return product_list

        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection:
                connection.close()


    @product_app.route('/<int:product_id>', methods=['GET'])
    def product_detail(product_id):
        """ [서비스] 제품 상세페이지 제품정보 가져오기
        Author:
            Ji Yoon Lee
        Args:
            - product_id (path parameter)
        Returns:
            - 200 :  
                { 
                    'message': 'SUCCESS',
                    'result': {
                        'product': 상품정보
                    }
                }
            - 400: "요청에 실패하였습니다"
        """
        connection = None
        try:
            connection = connect_db()
            if connection:
                product_service = ProductService()

                product_detail = product_service.get_product_detail(product_id, connection)

            return product_detail

        except Exception as e:
            if connection:
                connection.rollback()
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()

    @product_app.route('/question/open', methods=['GET'])
    @login_decorator
    def get_question_open():
        """ [서비스] 제품 상세페이지에서 질문 올릴 때 질문유형 선택 드롭박스
        Author:
            Ji Yoon Lee
        Args:
            - token(str): 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
        Returns:
            - 200 :  
                { 
                    'message': 'SUCCESS',
                    'result': {
                        'data': 질문 유형 목록
                    }
                }
            - 400: "요청에 실패하였습니다"
        Note:
            회원만 질문을 남길 수 있음
        """
        connection = None
        try:
            connection = connect_db()
            if connection:
                product_service = ProductService()
                type_list       = product_service.get_question_open(connection)

                return type_list

        except Exception as e:
            if connection:
                connection.rollback()
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()


    @product_app.route('/<int:product_id>/question', methods=['GET'])
    @user_decorator
    def get_product_qna(product_id):
        """ [서비스] 제품 상세페이지에서 해당 상품 관련 질문 답변
        Author:
            Ji Yoon Lee
        Args:
            - token(str): 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
            - product_id (path parameter)
            - limit(int): 한 페이지에 보여질 게시물 수 (질문기준 갯수)
            - offset(int): 페이지 이동 시, 몇번째 게시물부터 보여줄 지
        Returns:
            - 200 :  
                { 
                    'message': 'SUCCESS',
                    'result': {
                        'data': {
                            질문 정보,
                            답변 정보(답변 있을시)
                        }
                    }
                }
            - 400: 존재하지 않는 상품의 경로로 들어온 경우 '잘못된 경로입니다'
        Note:
            - token 유무 상관없이 제품 상페페이지 접근 가능.
            - 단, token이 있고 해당 유저가 상품 질문을 남긴 경우, 자신이 등록한 글과 해당 답변은 열람 가능
            - 글 등록시 공개로 등록된 글은 본인의 글 아니여도 누구나 열람 가능
            - 자신의 아이디와 판매자의 브랜드 이름은 공개
            - 다른 회원이 올린 비공개 게시물은 아이디 부분 비공개처리 
        """
        connection = None
        try: 
            # 회원인지 비회원인지 확인. 회원이라면 회원 특정.
            if "token_info" in g:
                user_id = g.token_info["user_id"]
            else:
                user_id = None

            info = {
                'user_id': user_id,
                'product_id': product_id,
                'limit': int(request.args.get("limit", 5)),
                'offset': int(request.args.get("offset", 0))
            }

            connection = connect_db()

            if connection:
                product_service = ProductService()
                product_qna = product_service.get_product_qna(info, connection)
                
                return product_qna

        except Exception as e:
            if connection:
                connection.rollback()
            raise ApiException(400, WRONG_URI_PATH)

        finally:
            if connection:
                connection.close()


    @product_app.route('/question', methods=['POST'])
    @login_decorator
    def post_product_qna():
        """ [서비스] 제품 상세페이지에서 질문 등록
        Author:
            Ji Yoon Lee
        Args:
            - token(str): 로그인 user의 token이 header에 담겨 들어와 로그인 유효성 검사를 거침
            - body(dict): 'questionType', 'content', 'isPrivate'(비공개글일시), 'productId'
        Returns:
            - 200 :  
                { 
                    'message': 'SUCCESS',
                    'result': {
                        'data': {
                            등록된 질문 id,
                            질문 로그 id
                        }
                    }
                }
            - 400: '요청에 실패하였습니다', 필수 parameter 미입력시 '** 정보를 입력해 주세요'
            - 401: '로그인이 필요합니다'
        """
        connection = None
        try: 
            user_id = g.token_info['user_id']
            data = request.json

            if user_id is None:
                raise ApiException(401, LOGIN_REQUIRED)
            if 'questionType' not in data:
                raise ApiException(400, SELECT_QUESTION_TYPE)
            if 'content' not in data:
                raise ApiException(400, CONTENT_MISSING)
            if 'productId' not in data:
                raise ApiException(400, PRODUCT_INFO_MISSING)

            connection = connect_db()
            question_info = {
                'question_type_id': data['questionType'],
                'contents': data['content'],
                'is_private': data.get('isPrivate', 1),
                'product_id': data['productId'],
                'user_id': user_id
            }

            product_service = ProductService()
            product_qna = product_service.post_product_qna(question_info, connection)
            connection.commit()
            
            return product_qna

        except ApiException as e:
            if connection:
                connection.rollback()
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()


    @product_app.route('/recommends', methods=['GET'])
    def get_other_products():
        """ [서비스] 판매자의 다른상품 5개 추천
        Author:
            Ji Yoon Lee
        Args:
            - query string: 'sellerId', 'productId'
        Returns:
            - 200 :  
                { 
                    'message': 'SUCCESS',
                    'result': {
                        'data': {
                            상품정보
                        }
                    }
                }
            - 400: '요청에 실패하였습니다', 필수 parameter 미입력시 '** 정보를 입력해 주세요'
        """
        connection = None
        try: 
            info = {
                "seller_id"  : int(request.args['sellerId']),
                "product_id" : int(request.args['productId'])
            }

            connection = connect_db()
            if connection:
                product_service = ProductService()
                products_list = product_service.get_other_products(info, connection)

                return products_list

        except Exception as e:
            if connection:
                connection.rollback()
            raise ApiException(400, REQUEST_FAILED)

        finally:
            if connection:
                connection.close()