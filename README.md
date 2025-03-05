#### Setup

You need to add following env vars on your project where you are integrating this package.
Depending on your requirement you should add any one of the following setup. Currently, the package support S3, Minio(ony in dev mode) and local storage.

```dotenv
STORAGE_URL=http://127.0.0.1:9000 # is used only for minio
LOCAL_STORAGE_BASE=./storage/pdf

# For local storage
STORAGE_TYPE=LOCAL
KEY=key
SECRET=keySecret
APP_ENV=dev
STORAGE_REGION=emptyString

# For s3 storage
STORAGE_TYPE=S3
KEY=s3SecretKey
SECRET=keySecret
APP_ENV=dev
STORAGE_REGION=aws-region

# For minio storage
STORAGE_TYPE=MINIO
KEY=minioSecretKey
SECRET=keySecret
APP_ENV=dev
STORAGE_REGION=aws-region

```

###### Demo
You can build and run docker-compose file to see the demo of the package. The docker-compose file is available in the root directory of the project.

```bash
docker-compose up
```
##### Tests
You can run the tests by running the following command inside poetry shell. Make sure you have installed the dependencies.

```bash
poetry run pytest
```

> For not test is only for local adapter. It will create a local file test the local adapter features and
> on complete it will delete the file from the local storage.

###### TODOs

- [ ] Create test cases for cloud storage.
- [x] ~~Remove cloudstorage dependency and use native sdks.~~
