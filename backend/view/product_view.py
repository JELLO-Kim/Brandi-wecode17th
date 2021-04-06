from flask          import request, Blueprint, jsonify, g
from db_connector   import connect_db
from service        import ProductService 
from responses      import *
from utils          import login_decorator, user_decorator
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
            - 200: { "message" : "SUCCESS",
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
        connection = None
        try:

            connection = connect_db()
            if connection:
                product_service = ProductService()

                product_detail  = product_service.get_product_detail(product_id, connection)

            return product_detail

        except Exception as e:
            raise ApiException(400, PAGE_NOT_FOUND)

        finally:
            if connection:
                connection.close()

    # @login_decorator
    @product_app.route('/question/open', methods=['GET'])
    def get_question_open():
        connection = None
        try:
            connection = connect_db()
            if connection:
                product_service = ProductService()
                type_list       = product_service.get_question_open(connection)

                return type_list

        except Exception as e:
            raise ApiException(400, WRONG_URI_PATH)

        finally:
            if connection:
                connection.close()


    # @user_decorator
    @product_app.route('/<int:product_id>/question', methods=['GET'])
    def get_product_qna(product_id):
        """
        로그인 한 회원은 user_id로 누군지 특정. QnA에 작성한 글 있으면 보이게 하기위해.
        로그인하지 않은 사용자도 접근 가능
        """
        connection = None
        try: 
            if "token_info" in g:
                user_id = g.token_info["user_id"]
            else:
                user_id = None
            info = {
                'user_id'    : user_id,
                'product_id' : product_id,
                'limit'      : int(request.args.get("limit", 5)),
                'offset'     : int(request.args.get("offset", 0))
            }
            connection = connect_db()
            if connection:
                product_service = ProductService()
                product_qna     = product_service.get_product_qna(info, connection)
                return product_qna
        except Exception as e:
            raise ApiException(400, WRONG_URI_PATH)
        finally:
            if connection:
                connection.close()



    # @login_decorator
    @product_app.route('/question', methods=['POST'])
    def post_product_qna():
        connection = None
        try: 
            user_id = g.token_info["user_id"]
            data    = request.json

            if user_id is None:
                raise ApiException(401, LOGIN_REQUIRED)

            if 'questionType' not in data:
                raise ApiException(400, SELECT_QUESTION_TYPE)
            
            if 'content' not in data:
                raise ApiException(400, INVALID_CONTENT)

            connection    = connect_db()
            question_info = {
                'question_type_id' : data['questionType'],
                'contents'         : data['content'],
                'is_private'       : data.get('isPrivate', 1),
                'product_id'       : data['productId'],
                'user_id'          : user_id,
            }

            product_service = ProductService()
            product_qna     = product_service.post_product_qna(question_info, connection)
            connection.commit()
            
            return {"data" : product_qna}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise ApiException(400, UPLOAD_FAILED)

        finally:
            if connection:
                connection.close()
        return Success



    @product_app.route('/recommends', methods=['GET'])
    def get_other_products():
        connection = None
        try: 
            info = {
                "seller_id"  : int(request.args['sellerId']),
                "product_id" : int(request.args['productId'])
            }

            connection = connect_db()
            if connection:
                product_service = ProductService()
                products_list   = product_service.get_other_products(info, connection)

                return products_list

        except Exception as e:
            raise ApiException(400, WRONG_URI_PATH)

        finally:
            if connection:
                connection.close()


    @product_app.route('/fileupload', methods=['POST'])
    def file_upload():
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id = AWS_ID,
                aws_secret_access_key = AWS_KEY
            )

            image       = request.files['filename']

            if image is None:
                raise ApiException(400, "FILE_NOT_ATTACHED")

            upload_time = (str(datetime.now()).replace(" ", "")).replace("-","_")
            image_type  = (image.content_type).split("/")[1]

            s3_client.upload_fileobj(
                image,
                "brandi-17th",
                upload_time+"."+image_type,
                ExtraArgs={
                    "ContentType": image.content_type
                }
            )

            image_url = "https://brandi-17th.s3.ap-northeast-2.amazonaws.com/" + upload_time + "." + image_type
            image_url = image_url.replace(" ", "")

            return {"custom_message" : OK, "result" : image_url}
        
        except Exception as e:
            raise ApiException(400, "UPLOAD_FAILED")
