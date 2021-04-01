"""email, password validators"""


def validate_email(data):
    """ 형식에 맞는 이메일을 체크하는 함수
    Args:
        data: 유저가 입력한 이메일
    Returns:
        False: '@', '.'이 임력한 이메일에 없으면 False 반환 해준다
        True: if 문에 안걸리면 True 반환 해준
    """
    if "@" not in data:
        return False
    if '.' not in data:
        return False
    return True


def validate_password(data):
    """ 형식에 맞는 패쓰워드를 헤크하는 함
    Args:
        data: 유저가 입력한 패쓰워드
    Returns:
        False: 패쓰워드 길이가 8글자보다 적으면 False 반환 해준다
        True: if 문에 안걸리면 True 반환 해준다
    """
    if len(data) < 8:
        return False
    return True
