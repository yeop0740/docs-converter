FROM public.ecr.aws/lambda/python:3.12

COPY .env requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY ./src/consumer.py ./src/S3Client.py ${LAMBDA_TASK_ROOT}

CMD [ "consumer.handle" ]
