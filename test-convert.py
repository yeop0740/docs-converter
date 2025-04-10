from markitdown import MarkItDown
import boto3
import io
import uuid
from boto3.session import Session

md = MarkItDown(enable_plugins=False)
result = md.convert("로그 설정.pdf")
tmp_file = io.BytesIO(result.text_content.encode('utf-8'))

session = Session(profile_name='profile')
s3 = boto3.client('s3', region_name = 'ap-northeast-2')

bucket_name = 'bucket'
key = str(uuid.uuid4())

s3.upload_fileobj(tmp_file, bucket_name, key)
