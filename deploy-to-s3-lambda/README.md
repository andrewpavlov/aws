
set parameters

```sh
export DEPLOY_LAMBDA_BUCKET_NAME=bucket-name
export AWS_PROFILE=my-aws-profile
export AWS_REGION=us-east-1
```

## Deploy using current sources

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

## Deploy using existing package (andrewp-public-resources)

```sh
aws cloudformation create-stack \
--stack-name deploy2s3 \
--template-body file://deploy-to-s3-lambda/deploy-lambda.yml \
--capabilities CAPABILITY_NAMED_IAM \
--profile $AWS_PROFILE \
--region $AWS_REGION
```
