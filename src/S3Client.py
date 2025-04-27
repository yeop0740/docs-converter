import logging
import boto3
from botocore.exceptions import ClientError
import io

class S3Client:
    __service_name = 's3'
    __region = 'ap-northeast-2'

    def __init__(self):
        self.__client = boto3.client(self.__service_name, self.__region)

    # 업로드를 위한 presigned-url 을 생성한다.
    def generate_upload_presigned_url(self, bucket_name, key, expires_in):
        return self.generate_presigned_url('put_object', bucket_name, key, expires_in)

    # 다운로드를 위한 presigned-url 을 생성한다.
    def generate_download_presigned_url(self, bucket_name, key, expires_in):
        return self.generate_presigned_url('get_object', bucket_name, key, expires_in)
    
    def generate_presigned_url(self, operation_name, bucket_name, key, expires_in):
        try:
            response = self.__client.generate_presigned_url(operation_name, Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=expires_in)

        except ClientError as e:
            logging.error(e)
            raise Exception("download presigned url generate error") # 확인 필요
        
        return response

    # 변환을 위한 객체를 다운로드한다.
    def download_object(self, bucket_name, key):

        try:
            response = self.__client.get_object(Bucket=bucket_name, Key=key)
            return response['Body']

        except ClientError as e:
            logging.error(e)
            error = e.response.get('Error', {})
            error_code = error.get('Code', 'Unknown')
            if (error_code == 'NoSuchKey'):
                raise Exception("not found error")
            
            raise  Exception("S3 download error")

    # 변환한 데이터를 저장한다.
    def save_object(self, contents, bucket, key, content_type):
        contents_in_buffer = io.BytesIO(contents)

        try:
            self.__client.upload_fileobj(Fileobj=contents_in_buffer, Bucket=bucket, Key=key, ExtraArgs={'ContentType': content_type})
        
        except ClientError as e:
            logging.error(e)

            raise Exception("S3 upload error")
