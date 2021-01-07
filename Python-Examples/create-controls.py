import boto3, argparse

# Global variables
regions = ["us-east-1"]

#  Create new custom controls in AWS Audit Manager
def create_controls(client):
    custom_controls = {}
    
    # create dictionary of existing custom controls to prevent duplicate creation and validation errors
    existing_custom_controls = {}
    controls = client.list_controls(
        controlType='Custom'
    )

    for control in controls['controlMetadataList']:
        id = control['id']
        name = control['name']
        existing_custom_controls[name] = id

    # Create custom control that uses AWS Config for source data
    # Control evaluates that instances are deployed only on approved EC2 AMIs
    control_name = 'Deploy EC2 on approved AMIs only'
    if control_name in existing_custom_controls:
        print(control_name + ' control already exists, skipping creation\n')
        custom_controls[control_name] = existing_custom_controls[control_name]
    else: 
        response_awsconfig = client.create_control(
            name=control_name,
            description='This control will gather evidence for AMIs not running on approved AMIs',
            controlMappingSources=[
                {
                    'sourceName': 'APPROVED_AMIS_BY_ID',
                    'sourceDescription': 'Deploy EC2 on Approved AMIs Only',
                    'sourceSetUpOption': 'System_Controls_Mapping',   # sets collection to automatic
                    'sourceType': 'AWS_Config',
                    'sourceKeyword': {
                        'keywordInputType': 'SELECT_FROM_LIST',
                        'keywordValue': 'APPROVED_AMIS_BY_ID'
                    },
                    'troubleshootingText': 'Add relevant troubleshooting text here'
                },
            ],
        )    
        custom_controls[response_awsconfig['control']['name']] = response_awsconfig['control']['id']

    # Create custom control that uses AWS Security Hub for source data.
    # Control audits that unused instances are removed from the system
    control_name = 'Terminate all stopped EC2 instances within 30 days'
    if control_name in existing_custom_controls:
        print(control_name + ' control already exists, skipping creation\n')
        custom_controls[control_name] = existing_custom_controls[control_name]
    else: 
        response_securityhub = client.create_control(
            name=control_name,
            description='This control will collect evidence for EC2 instances that are stopped for more then 30 days without being terminated',
            controlMappingSources=[
                {
                    'sourceName': 'EC2.4',
                    'sourceDescription': 'Terminate all stopped EC2 instances within 30 days',
                    'sourceSetUpOption': 'System_Controls_Mapping',   # sets collection to automatic
                    'sourceType': 'AWS_Security_Hub',
                    'sourceKeyword': {
                        'keywordInputType': 'SELECT_FROM_LIST',
                        'keywordValue': 'EC2.4'
                    },
                    'troubleshootingText': 'Add relevant troubleshooting text here'
                },
            ],
        )
        custom_controls[response_securityhub['control']['name']] = response_securityhub['control']['id']

    # Create custom control that uses AWS API calls for source data.
    # Control audits existing IAM users daily
    control_name = 'Maintain a daily list of all IAM user accounts'
    if control_name in existing_custom_controls:
        print(control_name + ' control already exists, skipping creation\n')
        custom_controls[control_name] = existing_custom_controls[control_name]
    else: 
        response_api = client.create_control(
            name=control_name,
            description='This control will generate evidence showing all IAM user accounts once daily',
            controlMappingSources=[
                {
                    'sourceName': 'iam_ListUsers',
                    'sourceDescription': 'Record all IAM user accounts daily',
                    'sourceSetUpOption': 'System_Controls_Mapping',   # sets collection to automatic
                    'sourceType': 'AWS_API_Call',
                    'sourceKeyword': {
                        'keywordInputType': 'SELECT_FROM_LIST',
                        'keywordValue': 'iam_ListUsers'
                    },
                    'sourceFrequency': 'DAILY',
                    'troubleshootingText': 'Add relevant troubleshooting text here'
                },
            ],
        )
        custom_controls[response_api['control']['name']] = response_api['control']['id']

    # Create custom control that uses AWS Cloudtrail for source data.
    # Control audits aws console logins
    control_name = 'Log all AWS console access'
    if control_name in existing_custom_controls:
        print(control_name + ' control already exists, skipping creation\n')
        custom_controls[control_name] = existing_custom_controls[control_name]
    else: 
        response_cloudtrail = client.create_control(
            name=control_name,
            description='This control will audit and collect evidence every time an IAM user account is used to sign into the AWS console',
            controlMappingSources=[
                {
                    'sourceName': 'signin_ConsoleLogin',
                    'sourceDescription': 'Audit AWS console logins',
                    'sourceSetUpOption': 'System_Controls_Mapping',   # sets collection to automatic
                    'sourceType': 'AWS_Cloudtrail',
                    'sourceKeyword': {
                        'keywordInputType': 'SELECT_FROM_LIST',
                        'keywordValue': 'signin_ConsoleLogin'
                    },
                    'troubleshootingText': 'Add relevant troubleshooting text here'
                },
            ],
        )
        custom_controls[response_cloudtrail['control']['name']] = response_cloudtrail['control']['id']

    # Create custom control that uses manual validation
    # Control audits if a list of authorized console users exists
    control_name = 'Validate Authorized System User List Exists'
    if control_name in existing_custom_controls:
        print(control_name + ' control already exists, skipping creation\n')
        custom_controls[control_name] = existing_custom_controls[control_name]
    else: 
        response_manual = client.create_control(
            name=control_name,
            description='This control gathers evidence on whether an authorized system user list exists',
            controlMappingSources=[
                {
                    'sourceName': 'APPROVED_CONSOLE_LOGIN_USERS',
                    'sourceDescription': 'Validate Authorized Console User list exists',
                    'sourceSetUpOption': 'Procedural_Controls_Mapping',   # sets collection to manual evaluation
                    'sourceType': 'MANUAL',
                    'troubleshootingText': 'Add relevant troubleshooting text here'
                },
            ],
        )
        custom_controls[response_manual['control']['name']] = response_manual['control']['id']
    
    # returns list of control ids to be added to custom framework
    return custom_controls


def main():
    # Allow optional pass in of local profile name. If no profile is passed then the default local profile is used
    parser = argparse.ArgumentParser(description='Create custom AWS Audit Manager controls')
    parser.add_argument('-p', '--profile', type=str, help = 'Name of AWS Profile to use')
    args = parser.parse_args()


    # Iterate through each region to deploy custom controls
    for region in regions:
        if args.profile is not None:
            session = boto3.Session(profile_name=args.profile)
            client = session.client('auditmanager', region_name=region)
        else:
            client = boto3.client('auditmanager', region_name=region)

    control_ids = create_controls(client)
    print('Custom Control IDs:\n')
    for control in control_ids:
        print('Control Name: ' + control)
        print('Control ID: ' + control_ids[control])
        print('')

if __name__ == "__main__":
    main()