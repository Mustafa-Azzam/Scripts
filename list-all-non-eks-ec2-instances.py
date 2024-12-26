#!/usr/bin/env python3

'''
### Steps To run this script:

1- Create Virtual Environment:
python3 -m venv myenv

2- Activate Virtual Environment:
source myenv/bin/activate

3- Install needed libraries:
pip install boto3 openpyxl

4- run your script
./script-name

5- Deactivate Virtual Environment:
deactivate

'''

import boto3
from openpyxl import Workbook

# Initialize EC2 client
ec2_client = boto3.client('ec2')

# Get all EC2 instances
all_instances = ec2_client.describe_instances()

# Get EKS-tagged instances
eks_instances = ec2_client.describe_instances(
    Filters=[
        {'Name': 'tag-key', 'Values': ['eks:cluster-name', 'karpenter.sh/nodepool']}
    ]
)

# Extract instance IDs
all_instance_ids = {i['InstanceId'] for r in all_instances['Reservations'] for i in r['Instances']}
eks_instance_ids = {i['InstanceId'] for r in eks_instances['Reservations'] for i in r['Instances']}

# Find non-EKS instances
non_eks_instance_ids = all_instance_ids - eks_instance_ids

# Gather details of non-EKS instances
non_eks_instances = []
for r in all_instances['Reservations']:
    for i in r['Instances']:
        if i['InstanceId'] in non_eks_instance_ids:
            # Extract instance name from tags
            instance_name = next(
                (tag['Value'] for tag in i.get('Tags', []) if tag['Key'] == 'Name'),
                'Unnamed'
            )
            non_eks_instances.append({
                'Instance ID': i['InstanceId'],
                'Instance Name': instance_name,
                'Instance Type': i['InstanceType'],
                'State': i['State']['Name'],
                'Launch Time': i['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
            })

# Print the results to the console
print("Non-EKS EC2 Instances:")
for instance in non_eks_instances:
    print(instance)

# Export the results to an Excel sheet
wb = Workbook()
ws = wb.active
ws.title = "Non-EKS EC2 Instances"

# Add header row
headers = ['Instance ID', 'Instance Name', 'Instance Type', 'State', 'Launch Time']
ws.append(headers)

# Add instance details
for instance in non_eks_instances:
    ws.append([instance[h] for h in headers])

# Save the Excel file
excel_file = 'non_eks_ec2_instances.xlsx'
wb.save(excel_file)

print(f"\nExported {len(non_eks_instances)} non-EKS instances to {excel_file}")
