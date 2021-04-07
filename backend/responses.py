class ApiException(Exception):
    def __init__(self, code, error_message, result=None):
        self.result = result
        self.code = code
        self.error_message = error_message

# 에러메세지
OK = "SUCCESS"  # GET 성공 : 200 Ok
CREATED = "성공적으로 등록되었습니다"  # POST 성공 : 201 Created
DELETED = "삭제되었습니다"  # DELETE (soft_delete) 성공 : 200 Ok
INVALID_USER = "유효하지 않은 유저입니다"  # 잘못된 token : 400 Bad request
INVALID_EMAIL = "형식에 맞는 이메일을 입력해 주세요"  # 이메일 validation 미충족 : 400 Bad request
INVALID_INPUT = "필수 정보가 입력되지 않았습니다"  # 필수정보가 입력되지 않았을 시 : 400 Bad request
INVALID_PASSWORD = '형식에 맞는 패스워드를 입력해 주세요' #패쓰워드 validation 미퐁족: 400 Bad request
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
NO_CART_EXISTS = '삭제하고싶은 카트가 없습니다' #주어진 product_id, color, size에 맞는 카트 가 없을때: 400 Bad request
COLOR_NOT_IN_INPUT = '컬러 key가 없습니다' #400 Bad request
SIZE_NOT_IN_INPUT = '시이즈 key가 없습니다' #400 Bad request
QUANTITY_NOT_IN_INPUT = 'quantity key가 없습니다' #400 Bad request
PRICE_NOT_IN_INPUT = 'price key가 없습니다' #400 Bad request

STOCK_NOT_IN_INPUT = 'stock key가 없습니다' #400 Bad request

PRODUCT_OPTION_NOT_IN_INPUT = 'product_optionkey가 없습니다' #400 Bad request

IS_SELLING_NOT_IN_KEYS = 'is_selling key가 없습니다' #400 Bad request

IS_DISPLAY_NOT_IN_KEYS = 'is_display key가 없습니다' #400 Bad request

DISCOUNT_RATE_NOT_IN_KEYS = 'discountRate key가 없습니다' #400 Bad request

PRODUCT_CATEGORY_NOT_IN_KEYS = 'product_category key가 없습니다' #400 Bad request

PRODUCT_NAME_NOT_IN_KEYS = 'product_name key가 없습니다' #400 Bad request

PRODUCT_THUMBNAIL_IMAGE_NOT_IN_KEYS = 'product_thumbnail_image key가 없습니다' #400 Bad request

PRODUCT_DETAIL_IMAGE_NOT_IN_KEYS = 'product_detail_image key가 없습니다' #400 Bad request

PRODUCT_OPTION_NOT_IN_KEYS = 'product_options key가 없습니다' #400 Bad request

INVALID_PRODUCT_OPTION = 'product_id에 해당하는 product_option_id이 아닙니다' #400 Bad request

PRICE_NOT_IN_KEYS = 'price key가 없습니다' #400 Bad request

PRODUCT_MINIMUM_NOT_IN_KEYS = 'product_minimum key가 없습니다' #400 Bad request

INVALID_INPUT_USERNAME = "아이디가 입력되지 않았습니다" # 아이디 입력되지 않았을 시 : 400 Bad request

INVALID_INPUT_PASSWORD = "패스워드가 입력되지 않았습니다" # 패스워드 입력되지 않았을 시 : 400 Bad request

INVALID_INPUT_KOREAN_BRAND_NAME = "셀러명이 입력되지 않았습니다" # 셀러명 미입력 시 :400 Bad request

INVALID_INPUT_ENGLISH_BRAND_NAME = "영문 셀러명이 입력되지 않았습니다" #영문 셀러명 미입력 시 : 400 Bad request

INVALID_INPUT_SELLER_CATEGORY = "셀러 정보를 선택하지 않았습니다" # 셀러 카테고리 미선택 시 : 400 Bad request

INVALID_INPUT_SERVICE_NUMBER = "고객센터 전화번호를 입력하지 않았습니다" # 고객센터 전화번호 미입력 시 : 400 Bad request

INVALID_INPUT_USER_TYPE_ID = 'user_type_id이 입력되지 않았습니다' #user_type_id 미입력 시: 400 Bad request

INVALID_INPUT_PHONE_NUMBER = '셀러 전화번호이 입력되지 않았습니다' #셀러 전화번호 미입력 시: 400 Bad request

PRODUCT_NAME_ALREADY_EXISTS = '셀러가 이미 있는 상품이름을 등록 할 수 없습니다' #셀러가 이미 등럭되있는 상품이름을 또 등록 시도 할때: 400 Bad request

DUPLICATED_USERNAME = '이미 존재하는 username입니다' #회원가입시 username이 이미 존재하면: 400 Bad request

DUPLICATED_EMAIL = '이미 존재하는 email입니다' #회원가입시 email이 이미 존재하면: 400 Bad request

DUPLICATED_KOREAN_BRAND_NAME = '이미 존재하는 korean_brand_name입니다' #셀러 회원가입시 korean_brand_name이 이미 존재하면: 400 Bad request

DUPLICATED_ENGLISH_BRAND_NAME = '이미 존재하는 english_brand_name입니다' #셀러 회원가입시 english_brand_name이 이미 존재하면: 400 Bad request

IS_NOT_SERVICE_USER = '서비스 유저가 아닙니다' #로그인시 user_type이 서비스 유저가 아닐때: 400 Bad request

IS_NOT_SELLER = '셀러 유저가 아닙니다' #로그인시 user_type이 셀러가 아닐때: 400 Bad request

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
INVALID_INPUT_USERNAME = "아이디가 입력되지 않았습니다" # 아이디 입력되지 않았을 시 : 400 Bad request
INVALID_INPUT_PASSWORD = "패스워드가 입력되지 않았습니다" # 패스워드 입력되지 않았을 시 : 400 Bad request
INVALID_INPUT_KOREAN_BRAND_NAME = "셀러명이 입력되지 않았습니다" # 셀러명 미입력 시 :400 Bad request
INVALID_INPUT_ENGLISH_BRAND_NAME = "영문 셀러명이 입력되지 않았습니다" #영문 셀러명 미입력 시 : 400 Bad request
INVALID_INPUT_SELLER_CATEGORY = "셀러 정보를 선택하지 않았습니다" # 셀러 카테고리 미선택 시 : 400 Bad request
INVALID_INPUT_SERVICE_NUMBER = "고객센터 전화번호를 입력하지 않았습니다" # 고객센터 전화번호 미입력 시 : 400 Bad request
INVALID_INPUT_USER_TYPE_ID = 'user_type_id이 입력되지 않았습니다' #user_type_id 미입력 시: 400 Bad request
INVALID_INPUT_PHONE_NUMBER = '셀러 전화번호이 입력되지 않았습니다' #셀러 전화번호 미입력 시: 400 Bad request
PRODUCT_NAME_ALREADY_EXISTS = '셀러가 이미 있는 상품이름을 등록 할 수 없습니다' #셀러가 이미 등럭되있는 상품이름을 또 등록 시도 할때: 400 Bad request
DUPLICATED_USERNAME = '이미 존재하는 username입니다' #회원가입시 username이 이미 존재하면: 400 Bad request
DUPLICATED_EMAIL = '이미 존재하는 email입니다' #회원가입시 email이 이미 존재하면: 400 Bad request
DUPLICATED_KOREAN_BRAND_NAME = '이미 존재하는 korean_brand_name입니다' #셀러 회원가입시 korean_brand_name이 이미 존재하면: 400 Bad request
DUPLICATED_ENGLISH_BRAND_NAME = '이미 존재하는 english_brand_name입니다' #셀러 회원가입시 english_brand_name이 이미 존재하면: 400 Bad request
IS_NOT_SERVICE_USER = '서비스 유저 아닙니다' #로그인시 user_type이 서비스 유저가 아닐때: 400 Bad request
IS_NOT_SELLER = '셀러 유저가 아닙니' #로그인시 user_type이 셀러가 아닐때: 400 Bad request
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
EXSISTING_MANAGER_NAME = "이미 존재하는 담당자 이름입니다"
EXSISTING_MANAGER_EMAIL = "이 이메일은 이미 해당 셀러 담당자의 이메일로 사용되었습니다."
EXSISTING_MANAGER_PHONE = "이 연락처는 이미 해당 셀러 담당자의 연락처로 사용되었습니다."

SERVICE_USER_NO_ACCESS = "일반 유저는 접근 권한이 없습니다"

MAX_LIMIT_MANAGER = "매니저 입력 최대치는 3명 입니다."

UPDATED = "정보를 수정하였습니다"
# 마스터 API에 user나 seller가 들어왔을 때
USER_NOT_MASTER = 'msater 계정이 아닙니다.' #400 Bad request
NOT_SELLER = "샐러를 선택해주세요."
NOT_ACTION = "액션 버튼을 선택해주세요."
NOT_SEARCH_ITEM = "필요한 검색창의 조건들이 없습니다."
IMAGE_URL_NOT_IN_KEYS = "이미지 url이 없습니다."
PRODUCT_ID_NOT_IN_KEYS = 'product_id가 없습니다'
DISCOUNT_PRICE_NOT_IN_KEYS = '할인 가격이 없습니댜'
DISCOUNT_START_NOT_IN_KEYS = '할인 시작 날짜가 없습니다'
DISCOUNT_END_NOT_IN_KEYS = '할인 끝나는 날짜가 없습니다'

PRODUCT_OPTION_NOT_EXISTING = "해당 옵션이 존재하지 않습니다."
ADDRESS_ALREADY_EXISTS = "이미 등록된 주소입니다."
NAME_MISSING = "이름을 입력해주세요."
PHONE_MISSING = "전화번호를 입력해주세요."
POSTAL_MISSING = "우편번호를 입력해주세요."
ADDRESS_MISSING = "주소를 입력해주세요."
ADDRESS_DETAIL_MISSING = "상세주소를 입력해주세요." 
EMAIL_MISSING = "이메일 주소를 입력해주세요."
ORDER_MISSING = "주문번호를 입력해주세요."
SHIPPING_MEMO_MISSING = "배송메모를 입력해주세요."
SHIPPING_INFO_MISSING = "배송지를 입력해주세요"
PRICE_MISSING = "가격을 확인해주세요."
PRODUCT_INFO_MISSING = "상품정보를 입력해주세요."
CONTENT_MISSING = "내용을 입력해주세요."



