class ApiException(Exception):
    def __init__(self, code, message, result=None):
        self.result = result
        self.code = code
        self.message = message


# 에러메세지
OK = "SUCCESS"  # GET 성공 : 200 Ok

CREATED = "성공적으로 등록되었습니다"  # POST 성공 : 201 Created

DELETED = "삭제되었습니다"  # DELETE (soft_delete) 성공 : 200 Ok

INVALID_USER = "유효하지 않은 유저입니다"  # 잘못된 token : 400 Bad request

INVALID_EMAIL = "형식에 맞는 이메일을 입력해 주세요"  # 이메일 validation 미충족 : 400 Bad request

INVALID_INPUT = "필수 정보가 입력되지 않았습니다"  # 필수정보가 입력되지 않았을 시 : 400 Bad request

INVALID_PASSWORD = '형식에 맞는 패쓰워드를 입력해 주세요' #패쓰워드 validation 미퐁족: 400 Bad request

USER_NOT_FOUND = "존재하지 않는 유저입니다"  # 로그인 시 존재하지 않는 email 입력 시 : 400 Bad request

USER_HAS_BEEN_DELETED = '유저가 삭제 되었습니다'

INVALID_TOKEN = "유효하지 않은 토큰 입니다"

# 로그인시 이메일은 존재하지만 비밀번호가 일치하지 않을 경우 : 400 Bad request
PASSWORD_MISMATCH = "비밀번호를 확인해 주세요"

PRODUCT_MISSING = "상품을 담아주세요"  # 결제/장바구니 진행 시 물건을 선택하지 않았을 때

# 중복을 허용하지 않는데 확인한 값이 이미 존재할 경우 : 400 Bad request ex) 회원가입 시 이메일, 셀러명, 브랜드명 등
DUPLICATED_INPUT = "이미 존재하는 값입니다"

LOGIN_REQUIRED = "로그인이 필요합니다"  # token이 필요한 기능에 token이 없을 시 : 401 Unauthorized

# master 전용 기능에 user나 seller의 토큰 혹은 seller의 전용 기능에 user의 token으로 접속할 시 : 403 Forbidden
ACCESS_DENIED = "접근 권한이 없습니다"

PAGE_NOT_FOUND = "존재하지 않는 페이지입니다"  # 잘못된 path parameter로 접근 시 : 404 Not Found

INTERNAL_SERVER_ERROR = "서버 요청 실패"  # backend 로직 에러 : 500 Internal Server Error

WRONG_URI_PATH = "잘못된 경로 입니다" # 존재하지 않는 uri 입력 : 잘못된 url 입력시 message=SUCCESS & result=None 으로 반한되는 것을 방지하기 위한 수단

NO_CURRENT_ORDER_EXISTS = '유저가 결제전인 오더가 없습니다' #유저가 결제전인 오더가 없을때: 400 Bad request

NO_CART_EXISTS = '카트가 없습니다' #주어진 product_id, color, size에 맞는 카트 가 없을때: 400 Bad request

COLOR_NOT_IN_INPUT = '컬러 key가 없습니다' #400 Bad request

SIZE_NOT_IN_INPUT = '시이즈 key가 없습니다' #400 Bad request

QUANTITY_NOT_IN_INPUT = 'quantity key가 없습니다' #400 Bad request

PRICE_NOT_IN_INPUT = 'price key가 없습니다' #400 Bad request

STOCK_NOT_IN_INPUT = 'stock key가 없습니다' #400 Bad request

PRODUCT_OPTION_NOT_IN_INPUT = 'product_optionkey가 없습니다' #400 Bad request

IS_SELLING_NOT_IN_KEYS = 'is_selling key가 없습니다' #400 Bad request

IS_DISPLAY_NOT_IN_KEYS = 'is_display key가 없습니다' #400 Bad request

IS_DISCOUNT_NOT_IN_KEYS = 'is_discount key가 없습니다' #400 Bad request

PRODUCT_CATEGORY_NOT_IN_KEYS = 'product_category key가 없습니다' #400 Bad request

PRODUCT_NAME_NOT_IN_KEYS = 'product_name key가 없습니다' #400 Bad request

PRODUCT_THUMBNAIL_IMAGE_NOT_IN_KEYS = 'product_thumbnail_image key가 없습니다' #400 Bad request

PRODUCT_DETAIL_IMAGE_NOT_IN_KEYS = 'product_detail_image key가 없습니다' #400 Bad request

PRODUCT_OPTION_NOT_IN_KEYS = 'product_options key가 없습니다' #400 Bad request

PRICE_NOT_IN_KEYS = 'price key가 없습니다' #400 Bad request

PRODUCT_MINIMUM_NOT_IN_KEYS = 'product_minimum key가 없습니다' #400 Bad request

INVALID_FILTER_CONDITION = "잘못된 검색조건입니다" #유효하지 않은 filter 조건이 들어왔을 경우 : 404

NOT_PROFILE = "프로필 사진이 입력되지 않았습니다"

NOT_DESCRIPTION = "셀러 한줄 소개란이 비어있습니다"

NOT_CALL_NUM = "고객센터 연락처를 입력해주세요"

NOT_CALL_NAME = "고객센터 명을 입력해 주세요"

NOT_CALL_START = "고객센터 영업시작 시간을 입력해 주세요"

NOT_CALL_END = "고객센터 영업종료 시간을 입력해 주세요"

NOT_POSTAL = "배송지 우편번호를 입력해 주세요"

NOT_ADDRESS = "배송지 주소를 입력해 주세요"

NOT_DETAIL_ADDRESS = "배송지 상세 주소를 입력해 주세요"

NOT_SHIPPING_DESCRIPTION = "배송 정보를 입력해 주세요"

NOT_ORDER_DESCRIPTION = "교환/환불 정보를 입력해 주세요"

SHORT_INPUT_SELLER = "10글자 이상 입력해 주세요"

NOT_MANAGER = "담당자 정보를 입력해 주세요"

NOT_MANAGER_NAME = "담당자 이름을 입력해 주세요"

NOT_MANAGER_NUMBER = "담당자 연락처를 입력해 주세요"

NOT_MANAGER_EMAIL = "담당자 이메일을 입력해 주세요"

EXSISTING_MANAGER = "이미 존재하는 담당자 정보입니다"

REQUEST_FAILED = "요청에 실패하였습니다"

SELECT_ADDRESS_TO_DELETE = "삭제할 주소를 선택해주세요" 
