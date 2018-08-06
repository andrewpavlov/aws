
# Node.JS web application starter

Set of stacks for web application based on

* Backend:
    - EC2 Nodejs
* FrontEnd:
    - EC2 Nodejs
    - S3
* Database:
    - MySQL

## Create EC2 resources (like security group)

```sh
aws cloudformation create-stack \
--stack-name refigure-ec2-res \
--template-body file://nodejs-web-app-starter/ec2-res.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Project,ParameterValue=refigure \
--profile refigure.dev \
--region us-east-1
```

## Create Launch Configuration

```sh
aws cloudformation create-stack \
--stack-name refigure-lc \
--template-body file://nodejs-web-app-starter/lc.yml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Project,ParameterValue=refigure \
ParameterKey=Configuration,ParameterValue=refigure.dev \
ParameterKey=KeyPair,ParameterValue=refigure.dev \
--profile refigure.dev \
--region us-east-1
```

Where
* Configuration - EC2 oparameters store value name with runtime launch configuration

### Launch configuration run-time parameters

Create "String" value and add any parameters  
```ParameterKey=ParameterValue``` (one per line)

* Required
    * SiteDir - EC2 local path (/var/www/$SiteDir/)
    * ServiceCmd - Service command (node /var/www/$SiteDir/$ServiceCmd)
* Optional
    * Route53
        * Domain/SubDomain - Register EC2 as SubDomain.Domain
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