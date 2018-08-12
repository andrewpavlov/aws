
# Node.JS web application starter

Set of stacks for web application based on

* Backend:
    - EC2 Nodejs
* FrontEnd:
    - EC2 Nodejs
    - S3
* Database:
    - MySQL

## Set properties

```
export AWS_PROFILE=my-account-name
export AWS_REGION=us-east-1
export PROJECT_NAME=my-project
export EC2_KEYPAIR=keypair
export PROJECT_VPC=my-vpc
```

## Create EC2 resources (like security group)

```sh
aws cloudformation create-stack \
--stack-name $PROJECT_NAME-ec2-res \
--template-body file://nodejs-web-app-starter/ec2-res.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Project,ParameterValue=$PROJECT_NAME \
--profile $AWS_PROFILE \
--region $AWS_REGION
```

## Create Launch Configuration (dev/qa/prod)

```sh
for stage in "dev" "qa" "prod"; do \
    aws cloudformation create-stack \
    --stack-name $PROJECT_NAME-$stage-lc \
    --template-body file://nodejs-web-app-starter/lc.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters \
    ParameterKey=Project,ParameterValue=$PROJECT_NAME \
    ParameterKey=KeyPair,ParameterValue=$EC2_KEYPAIR \
    --profile $AWS_PROFILE \
    --region $AWS_REGION; \
done
```

Where:
* KeyPair - EC Key Pair for SSH access

### Launch configuration run-time parameters

Create Parameters Store "String" $PROJECT_NAME-#stage-lc value and add any parameters  
```ParameterKey=ParameterValue``` (one per line)

* Required
    * ServiceCmd - Service command (node /var/www/$PROJECT_NAME/$ServiceCmd)
* Optional
    * MySQL
        * MyUser - use this instead of root
        * MyPassword - for both root and MyUser
        * MyDB - initial DB for local MySQL
    * Duplicated MySQL data from
        * FromHost - import database from another MySQL
        * FromPort - 3306 by default
        * FromUser - use another user on source MySQL
        * FromPassword - use another password on source MySQL
        * FromDB - use another database on source MySQL
    * EFS
        * EfsId - EFS Id (will be mounted as /mnt/efs/)
        * EfsPath - Will be linked to /files


## Create EC2 (dev/qa/prod)

```sh
for stage in "dev" "qa" "prod"; do \
    aws cloudformation create-stack \
    --stack-name $PROJECT_NAME-$stage \
    --template-body file://nodejs-web-app-starter/as.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters \
    'ParameterKey=ASOptions,ParameterValue="0,0,1"' \
    --profile $AWS_PROFILE \
    --region $AWS_REGION; \
done
```

## Create Target Groups for Appliation Load Balancer (dev/qa/prod)

```sh
for stage in "dev" "qa" "prod"; do \
    aws cloudformation create-stack \
    --stack-name $PROJECT_NAME-$stage-tg \
    --template-body file://nodejs-web-app-starter/tg.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters \
    ParameterKey=VpcId,ParameterValue=$PROJECT_VPC \
    --profile $AWS_PROFILE \
    --region $AWS_REGION; \
done
```

## Create pipeline resources

```sh
aws cloudformation create-stack \
--stack-name $PROJECT_NAME-pipeline-res \
--template-body file://nodejs-web-app-starter/pipeline-res.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Project,ParameterValue=$PROJECT_NAME \
--profile $AWS_PROFILE \
--region $AWS_REGION
```
