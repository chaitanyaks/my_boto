import boto3

client=boto3.client('iam')
iam = boto3.resource('iam')
user_name=''
serial_number=''

def deactivate_mfa_device(user_name,serial_number):
	response = client.deactivate_mfa_device(UserName=user_name,SerialNumber=serial_number)
	print "done"
def get_mfa_serial_number(user_name):
        paginator = client.get_paginator('list_virtual_mfa_devices')
        response = client.list_virtual_mfa_devices(AssignmentStatus='Any')
        sno=''
        for key, value  in response.items():
                if key=='VirtualMFADevices':
                        for i in value:
                                for k,v in i.items():
                                        if k=='SerialNumber':
                                                sno=v
                                        if k == 'User':
                                                for u,uv in v.items():
                                                        if u =='UserName' and uv == user_name:
                                                                serial_number=sno
                                                                return sno
deactivate_mfa_device('user1',get_mfa_serial_number('user1'))
