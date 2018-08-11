
set parameters

```
export DEPLOY_LAMBDA_BUCKET_NAME=bucket-name
export AWS_PROFILE=my-aws-profile
export AWS_REGION=us-east-1
```

Create bucket for lambda

```sh
aws s3 mb s3://$DEPLOY_LAMBDA_BUCKET_NAME \
--profile $AWS_PROFILE \
--region $AWS_REGION
```

Upload lambda (python & pip & virtualenv should be instaled)

```sh
./upload-lamba $DEPLOY_LAMBDA_BUCKET_NAME deploy-to-s3-lambda.zip $AWS_PROFILE $AWS_REGION
```
