#### Setup

You need to add following env vars on your project where you are integrating this package.
Depending on your requirement you ashould add any one of the following setup. Currently the package support S3, Minio(ony in dev mode) and local storage.

```dotenv
STORAGE_URL=http://127.0.0.1:9000 # is used only for minio
LOCAL_STORAGE_BASE=./storage/pdf

# For local storage
STORAGE_TYPE=LOCAL
## for local storage key is the path to storage directory.
KEY=../storage/pdf
SECRET=keySecret
APP_ENV=dev
STORAGE_REGION=emptyString

# For s3 storage
STORAGE_TYPE=S3
## for local storage key is the path to storage directory.
KEY=s3SecretKey
SECRET=keySecret
APP_ENV=dev
STORAGE_REGION=aws-region

# For minio storage
STORAGE_TYPE=MINIO
## for local storage key is the path to storage directory.
KEY=minioSecretKey
SECRET=keySecret
APP_ENV=dev
STORAGE_REGION=aws-region

```

> More info to be added later.

###### TODOs

- Create test cases.
- Remove cloudstorage dependency and use native sdks.
