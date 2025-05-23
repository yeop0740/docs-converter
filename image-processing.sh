#!/bin/bash

export $(egrep -v '^#' .env | xargs)

CONTENTS_CONSUMER_LAMBDA_REPOSITORY_NAME_WITH_STAGE=$CONTENTS_CONSUMER_LAMBDA_REPOSITORY_NAME-$STAGE

aws ecr get-login-password --region ap-northeast-2 --profile $PROFILE | docker login --username AWS --password-stdin $CONTENTS_CONSUMER_LAMBDA_REPOSITORY_URI

docker buildx build --platform linux/amd64 -t $CONTENTS_CONSUMER_LAMBDA_REPOSITORY_NAME_WITH_STAGE .

docker tag $CONTENTS_CONSUMER_LAMBDA_REPOSITORY_NAME_WITH_STAGE:latest $CONTENTS_CONSUMER_LAMBDA_REPOSITORY_URI/$CONTENTS_CONSUMER_LAMBDA_REPOSITORY_NAME_WITH_STAGE:latest

docker push $CONTENTS_CONSUMER_LAMBDA_REPOSITORY_URI/$CONTENTS_CONSUMER_LAMBDA_REPOSITORY_NAME_WITH_STAGE:latest
