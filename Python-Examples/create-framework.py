import boto3, argparse

control_ids = [
    "bcb17ce9-7aba-42e2-b7af-242d22991c3c",
    "73195530-3606-40f2-bb46-ce185a663ae4",
    "d948bdf3-f46a-4ee2-aa44-6b70f3ab2795",
    "3745a3bf-41e2-4395-808b-f8354f725306",
    "ee4c8627-4f5a-46cc-bff9-8cc3a34aac5d"
]

framework_name = 'Enterprise Custom Framework Demo'

def create_framework(client):
# create dictionary of existing custom frameworks to prevent duplicate creation and validation errors
    existing_custom_frameworks = {}
    frameworks = client.list_assessment_frameworks(
        frameworkType='Custom'
    )

    for framework in frameworks['frameworkMetadataList']:
        id = framework['id']
        name = framework['name']
        existing_custom_frameworks[name] = id


# Create Custom Framework
    framework_controls = []
    for id in control_ids:
        control = {'id': id}
        framework_controls.append(control)        

    if framework_name in existing_custom_frameworks:
        print('Custom framework already exists, skipping creation')
    else: 
        response = client.create_assessment_framework(
            name=framework_name,
            description='This is a demo framework with both custom and standard controls included',
            complianceType='Custom-Internal',
            controlSets=[
                {
                    'name': 'Custom-Internal-Controls',
                    'controls': framework_controls
                },
            ]
        )
        print("New Framework created: " + response['framework']['id'])

def main():
    # Allow optional pass in of local profile name. If no profile is passed then the default local profile is used
    parser = argparse.ArgumentParser(description='Create custom AWS Audit Manager controls')
    parser.add_argument('-p', '--profile', type=str, help = 'Name of AWS Profile to use')
    args = parser.parse_args()

    # List of regions to create custom controls in. Add or remove regions as desired
    regions = ["us-east-1"]

    # Iterate through each region to deploy custom controls
    for region in regions:
        if args.profile is not None:
            session = boto3.Session(profile_name=args.profile)
            client = session.client('auditmanager', region_name=region)
        else:
            client = boto3.client('auditmanager', region_name=region)

    create_framework(client)

if __name__ == "__main__":
    main()