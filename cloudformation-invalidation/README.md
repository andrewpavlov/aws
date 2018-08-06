Create stack

```sh
aws cloudformation create-stack \
--stack-name cloudfront-invalidation \
--template-body file://cloudfront-invalidation.yml \
--capabilities CAPABILITY_NAMED_IAM \
--profile AWS_PROFILE \
--region AWS_REGION
```
