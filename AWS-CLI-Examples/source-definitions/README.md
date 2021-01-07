# Source Definitions
Each of the json files are intended to describe the Audit Manager data sources for individual controls or the control sets for custom frameworks. Each of the files is passed into various AWS CLI commands

* api-example.json - creates a AWS API based data-source that gathers a list of IAM users daily

* awsconfig-example.json - creates an AWS Config based data-source that gathers a list of EC2 instances using unapproved AMIs. Note this requires configuring the Approved-AMIs-by-id Config Rule with approved amiIds

* cloudtrail-example.json - creates a Cloudtrail based data-source that creates evidence everytime an IAM user performs a console logon

* control-sets.json - a list of specific controls, specified by unique control id, that are added to the custom framework we create. Note the file here has example IDs that must be replaced with the ID of the controls in your specific AWS account

* manual-example.json - creates a manual data source where evidence must be manually uploaded by end users

* securityhub-example.json - creates a Security Hub based data-source that creates evidence if an EC2 instance is stopped for more then 30 days without being terminated
