#!/bin/bash

echo "move to src directory"
cd src

echo "remove package directory"
rm -rf package

echo "remove zip file"
rm contents-consumer-lambda.zip

echo "make package directory"
mkdir package

echo "ls -l"
ls -l

echo "pip install"
pip install -r ../requirements.txt --target ./package
# --target ./package \
# --platform manylinux2014_x86_64 \
# --python-version 310 \
# --only-binary=:all: \


echo "remove pycache"
rm -rf ./package/__pycache__

echo "move to package directory"
cd package

echo "workDir : $(pwd)"

echo "zip"
zip -r ../contents-consumer-lambda.zip .

echo "move to src directory"
cd ../

echo "add files"
zip contents-consumer-lambda.zip consumer.py S3Client.py

echo "remove package"
rm -rf package
