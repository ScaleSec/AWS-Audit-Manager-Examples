#!/bin/bash

# Create a control with an AWS API data source
aws auditmanager create-control \
  --name "Maintain a daily list of all IAM user accounts" \
  --description "This control will generate evidence showing all IAM user accounts once daily" \
  --control-mapping-sources file://source-definitions/api-example.json \

# Create a control with an AWS Config data source
aws auditmanager create-control \
  --name "Deploy EC2 on approved AMIs only" \
  --description "This control will gather evidence for AMIs not running on approved AMIs." \
  --control-mapping-sources file://source-definitions/awsconfig-example.json \

# Create a control with a Cloudtrail data source
aws auditmanager create-control \
  --name "Log all AWS console access" \
  --description "This control will audit and collect evidence every time an IAM user account is used to sign into the AWS console." \
  --control-mapping-sources file://source-definitions/cloudtrail-example.json \

# Create a control with Manual Evidence Requirement
aws auditmanager create-control \
  --name "Validate Authorized System User List Exists" \
  --description "This control gathers evidence on whether an authorized system user list exists" \
  --control-mapping-sources file://source-definitions/manual-example.json \

# Create a control with a SecurityHub data source
aws auditmanager create-control \
  --name "Terminate all stopped EC2 instances within 30 days" \
  --description "This control will collect evidence for EC2 instances that are stopped for more then 30 days without being terminated." \
  --control-mapping-sources file://source-definitions/securityhub-example.json \
