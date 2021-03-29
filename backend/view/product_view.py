from flask          import request, Blueprint, jsonify
from db_connector   import connect_db
from service        import ProductService 
from errors         import *

class ProductView:
    product_app = Blueprint('product_app', __name__, url_prefix='/products')

    # products의 카테고리 선택 목록에 대한 로직
    @product_app.route('/category', methods=['GET'])
    def products_category():
        connection = None
        try:
            connection = connect_db()
            produts_category_service = ProductService()
            result = produts_category_service.products_category(connection)

            return result

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
        MINIMUM_CATEGORY_NUMBER = 4
        MAXIMUM_CATEGORY_NUMBER = 5
        connection = None
        try:
            connection = connect_db()
            products_service = ProductService()
            filter_data = {}
            page_condition = {}
            category    = request.args.get('category', None)
            limit       = request.args.get('limit', None)
            offset      = request.args.get('offset', None)

            # filtering 조건으로 들어올 category의 값이 허용 범위를 넘었을 경우 에러 반환
            if category is not None:
                if int(category) < MINIMUM_CATEGORY_NUMBER or int(category) > MAXIMUM_CATEGORY_NUMBER :
                    raise ApiException(404, INVALID_FILTER_CONDITION)
                filter_data['category'] = category

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

            result = products_service.products_list(filter_data, connection, page_condition)

            return result

        except Exception as e:
            if connection:
                connection.rollback
            raise e
        finally:
            if connection:
                connection.close()