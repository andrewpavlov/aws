Create stack

```sh
export AWS_PROFILE=my-account-name
export AWS_REGION=us-east-1
export PROJECT_NAME=my-project
```

```sh
aws cloudformation create-stack \
--stack-name $PROJECT_NAME-invalidation-lambda \
--template-body file://cloudfront-invalidation/deploy-lambda.yml \
--capabilities CAPABILITY_NAMED_IAM \
--profile $AWS_PROFILE \
--region $AWS_REGION
```
