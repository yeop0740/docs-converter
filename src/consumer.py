import json
from S3Client import S3Client
from markitdown import MarkItDown
from dotenv import load_dotenv
import os
from urllib import parse

load_dotenv()

converted_prefix = os.getenv("CONVERTED_BUCKET_PREFIX")

s3_client = S3Client()
md = MarkItDown(enable_plugins=False)

def handle(event, context):
    batch_item_failures = []
    sqs_batch_response = {}
    messages = event['Records']
    print(f'[messages] {messages}')

    for message in messages:
        body = message['body']
        events = json.loads(body)
        print(f'[events] {events}')

        if ('Records' in events):
            for ev in events['Records']:

                if ev['s3']['object']['size'] > 0:
                    try:
                        bucket_name = ev['s3']['bucket']['name']
                        key = ev['s3']['object']['key']
                        converted_key = key.replace('+', '%20')
                        decoded_key = parse.unquote(converted_key)
                        path = decoded_key.split(sep='/', maxsplit=1)
                        sub_path = path[1:]
                        sub_path.insert(0, converted_prefix)
                        new_key = '/'.join(sub_path)

                        object = s3_client.download_object(bucket_name, decoded_key)
                        convertedObject = md.convert(object)
                        convertedObjectToString = convertedObject.text_content.encode('utf-8')

                        s3_client.save_object(convertedObjectToString, bucket_name, new_key, 'text/markdown')

                    except Exception as e:
                        print(f'[consumer] {e}')
                        if 'not found error' not in e.args:
                            batch_item_failures.append({'itemIdentifier': message['messageId']})

    sqs_batch_response["batchItemFailures"] = batch_item_failures
    return sqs_batch_response
