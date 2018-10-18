
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

```sh
export AWS_PROFILE=my-account-name
export AWS_REGION=us-east-1
export PROJECT_NAME=my-project
export EC2_KEYPAIR=keypair
export EC2_IMAGEID=ami-da05a4a0
export EC2_INSTANCETYPE=t2.micro
export PROJECT_VPC=my-vpc
export TG_HEALTHCHECK_PATH=/
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
    ParameterKey=ImageId,ParameterValue=$EC2_IMAGEID \
    ParameterKey=InstanceType,ParameterValue=$EC2_INSTANCETYPE \
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

## To unlink EC2 stack (previously created) from LaunchConfiguration stack

```sh
export EC2_LC=.... (output value from launch configuration stack)
export stage=... (dev/qa/prod)
aws cloudformation update-stack \
--stack-name $PROJECT_NAME-$stage \
--template-body file://nodejs-web-app-starter/as.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
'ParameterKey=ASOptions,ParameterValue="0,0,1"' \
ParameterKey=LC,ParameterValue=$EC2_LC \
--profile $AWS_PROFILE \
--region $AWS_REGION;
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
    ParameterKey=HealthCheckPath,ParameterValue=$TG_HEALTHCHECK_PATH \
    --profile $AWS_PROFILE \
    --region $AWS_REGION; \
done
```

## Create resources for static content (client-side tpl web-app) if needed

```sh
for stage in "dev" "qa" "prod"; do \
    aws cloudformation create-stack \
    --stack-name $PROJECT_NAME-$stage-static \
    --template-body file://nodejs-web-app-starter/static.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters \
    ParameterKey=Project,ParameterValue=$PROJECT_NAME \
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

## Create pipeline resources for ec2 based project if needed

```sh
aws cloudformation create-stack \
--stack-name $PROJECT_NAME-pipeline-ec2-res \
--template-body file://nodejs-web-app-starter/pipeline-ec2-res.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Project,ParameterValue=$PROJECT_NAME \
--profile $AWS_PROFILE \
--region $AWS_REGION
```
