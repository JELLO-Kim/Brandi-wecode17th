import boto3

from flask import Flask, request, Blueprint, jsonify
from responses import *
from datetime import date, datetime
from config import AWS_ID, AWS_KEY
    
    
class ServiceView:
    service_app = Blueprint('service_app', __name__, url_prefix='/services')
    
    @service_app.route('/fileupload', methods=['POST'])
    def file_upload():
        try:
            # data = request.json
            # folder = data["folder"]

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
            path = "Product/" + upload_time+"."+image_type

            reponse = s3_client.upload_fileobj(
                image,
                "brandi-17th",
                path,
                ExtraArgs={
                    "ContentType": image.content_type
                }
            )

            image_url = "https://brandi-17th.s3.ap-northeast-2.amazonaws.com/" + path
            image_url = image_url.replace(" ", "")

            return {"custom_message" : OK, "result" : image_url}
        
        except Exception as e:
            raise ApiException(400, "UPLOAD_FAILED")