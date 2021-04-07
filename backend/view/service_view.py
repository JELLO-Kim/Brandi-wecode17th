import boto3

from flask import request, Blueprint
from responses import *
from datetime import datetime
from config import AWS_ID, AWS_KEY
    
    
class ServiceView:
    service_app = Blueprint('service_app', __name__, url_prefix='/services')
    
    @service_app.route('/fileupload', methods=['POST'])
    def file_upload():
        """ [서비스] 이미지 업로드
        Author:
            Ji Yoon Lee
        Args:
            filename(local photo address)
        Returns:
            - 200: 
                {
                    'message': 'SUCCESS',
                    'result': 이미지 url
                }
            -400: 업로드 실패시 '요청에 실패하였습니다'
        Note:
            order 테이블에 status=1로 장바구니에 담겨있는 상품들이 결제되므로 patch 함수로 결제되는 상품들만 status=2 로 변경.
        """
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id = AWS_ID,
                aws_secret_access_key = AWS_KEY
            )

            image = request.files['filename']

            if image is None:
                raise ApiException(400, 'FILE_NOT_ATTACHED')

            upload_time = (str(datetime.now()).replace(' ', '')).replace('-','_')
            image_type = (image.content_type).split('/')[1]
            path = 'Product/' + upload_time+'.'+image_type

            s3_client.upload_fileobj(
                image,
                'brandi-17th',
                path,
                ExtraArgs={
                    'ContentType': image.content_type
                }
            )

            image_url = 'https://brandi-17th.s3.ap-northeast-2.amazonaws.com/' + path

            return image_url
        
        except Exception as e:
            raise ApiException(400, REQUEST_FAILED)