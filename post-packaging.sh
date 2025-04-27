#!/bin/bash

# aws cli, credential 설정이 되어 있는 환경이라고 가정
ROOT=src

# 환경변수 로딩
export $(egrep -v '^#' .env | xargs)

# zip 파일을 s3 에 업로드
function copy_file_to_bucket() {
  local response contents_consumer_lamdba_bucket zip_file_path key profile
  
  contents_consumer_lamdba_bucket="$CONTENTS_CONSUMER_LAMBDA_BUCKET-$STAGE"
  zip_file_path="$ROOT/$CONTENTS_CONSUMER_LAMBDA_ZIP_FILE_NAME"
  key="$CONTENTS_CONSUMER_LAMBDA_KEY-$STAGE"
  profile="$AWS_PROFILE"

#   echo "contents_consumer_lamdba_bucket : $contents_consumer_lamdba_bucket"
#   echo "zip file path : $zip_file_path"
#   echo "key : $key"
#   echo "profile : $profile"

  response=$(aws s3api put-object \
    --bucket $contents_consumer_lamdba_bucket \
    --body $zip_file_path \
    --key $key \
    --profile $profile)

  # shellcheck disable=SC2181
  if [[ ${?} -ne 0 ]]; then
    errecho "ERROR: AWS reports put-object operation failed.\n$response"
    rm -rf "$ROOT/package"
    return 1
  fi
}

copy_file_to_bucket

## 람다 업데이트 -> code deploy 로 자동화 시도(s3 update event)
