# AWS Audit Manager - Custom Control and Framework creation via Python and Boto3
These scripts provide examples of how to create custom controls and frameworks in AWS Audit Manager using the Boto3

Make sure you have updated your Boto3 to a version that supports Audit Manager.

## Create Custom Controls with the CLI
Customize the controls found in create-controls.py file or leave the default examples

Execute `python3 create-controls.py` in each region and account you wish to create the controls in

Note if you want to pass in a specific AWS profile for execution you can add --profile to the end of the command

## Create Custom Framework with the CLI
Update the `control_ids` list variable in create-framework.py to include the unique ids for the controls outputted by the create-controls.py execution above.

Execute `python3 create-framework.py` in each region and account you wish to create the framework in

Note if you want to pass in a specific AWS profile for execution you can add --profile to the end of the command


