#!/bin/bash

# Create new framework from scratch. 
# NOTE YOU WILL NEED TO ADD THE ACCOUNT SPECIFIC CONTROL IDS TO THE CONTROL_SETS.JSON FILE
aws auditmanager create-assessment-framework \
  --name "Enterprise Custom Framework Demo" \
  --description "This is a demo framework with both custom and standard controls included" \
  --control-sets file://source-definitions/control-sets.json

