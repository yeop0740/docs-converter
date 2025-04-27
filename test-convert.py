from markitdown import MarkItDown
import boto3
import io
import uuid
from boto3.session import Session
from dotenv import load_dotenv
import os

load_dotenv()

profile_name = os.getenv("PROFILE")
region_name = os.getenv("AWS_REGION")
bucket_name = os.getenv("CONTENTS_BUCKET")

md = MarkItDown(enable_plugins=False)
result = md.convert("로그 설정.pdf")
tmp_file = io.BytesIO(result.text_content.encode('utf-8'))

session = Session(profile_name=profile_name)
s3 = boto3.client('s3', region_name=region_name)
key = str(uuid.uuid4())

s3.upload_fileobj(tmp_file, bucket_name, key, {'ContentType': 'text/markdown'})

print(f"s3://{bucket_name}/{key} 업로드 완료")
