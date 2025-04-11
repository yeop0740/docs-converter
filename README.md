# docs-converter

## test-convert.py 를 실행하려면

**requirements**
- python 설치(3버전)
- aws cli 설치
- aws configure 명령어로 자격 증명 설정

레포 다운
```
git clone <repository>
```

버킷 명, 리전 명, aws configure 로 등록한 프로필 명을 입력
```.env
AWS_PROFILE=
AWS_REGION=
AWS_BUCKET_NAME=
```

실행 환경 설정
```
pip istall -r requirments.txt
```

스크립트 실행
```
python test-convert.py
```

## src/main 서버를 실행하려면..
```shell
uvicorn src.main:app --reload
```

`http://127.0.0.1:8000/docs`, `http://127.0.0.1:8000/redoc` 두 API 문서를 자동으로 만들어 준다!
