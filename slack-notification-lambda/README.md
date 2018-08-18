
## Set parameters

```sh
export SLACK_WEBHOOK=url (does not include host)
export SLACK_CHANNEL=channel-name (e.g. #general)
export SLACK_USERNAME=username (optional)
export SLACK_ICON=icon (optional - def :icon:)
export AWS_PROFILE=my-aws-profile
export AWS_REGION=us-east-1
```

## Deploy using existing package (andrewp-public-resources)

```sh
aws cloudformation create-stack \
--stack-name slack-notification \
--template-body file://slack-notification-lambda/deploy-lambda.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=WebHook,ParameterValue=$SLACK_WEBHOOK \
ParameterKey=Channel,ParameterValue=$SLACK_CHANNEL \
ParameterKey=Username,ParameterValue=$SLACK_USERNAME \
ParameterKey=Icon,ParameterValue=$SLACK_ICON \
--profile $AWS_PROFILE \
--region $AWS_REGION
```
