# AWS Audit Manager - Custom Control and Framework creation via AWS CLI
These scripts provide examples of how to create custom controls and frameworks in AWS Audit Manager using the AWS CLI

Make sure you have updated your AWS CLI to a version that supports Audit Manager. Also the examples assume a default AWS profile and region have been configured. If not you may need to add the --profile and --region flag to the examples

## Create Custom Controls with the CLI
Customize the controls found in the ./source-definitions directory or use the examples
Execute `create-controls.sh` in each region and account you wish to create the controls in

## Create Custom Framework with the CLI
Update the the ./source-definitions/control-sets.json file to include the unique IDs that you want to attach to the custom framework. You can find the IDs by running `aws auditmanager list-controls --control-type Custom` or `aws auditmanager list-controls --control-type Standard`

Execute `create-framework.sh` in each region and account you wish to create the framework in. Note that the control IDs in the control-sets.json will be unique per region.

