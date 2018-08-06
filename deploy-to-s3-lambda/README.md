Create bucket for lambda

```sh
aws s3 mb s3://BUCKET_NAME \
--profile AWS_PROFILE \
--region AWS_REGION
```

Upload lambda (python & pip & virtualenv should be instaled)

```sh
./upload-lamba BUCKET_NAME deploy-to-s3-lambda.zip AWS_PROFILE AWS_REGION
```
