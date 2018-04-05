import boto3

client=boto3.client('iam')
iam = boto3.resource('iam')
user_name=''
serial_number=''

def mfa_disassociate(user_name,serial_number):
	print user_name,serial_number
	mfa_device = iam.MfaDevice(user_name,serial_number)
	response = mfa_device.disassociate()
	return response

def get_mfa_serial_number(user_name):
        paginator = client.get_paginator('list_virtual_mfa_devices')
        response = client.list_virtual_mfa_devices(AssignmentStatus='Any')
#       response_iam = iam.list_virtual_mfa_devices(AssignmentStatus='Any')
        sno=''
        for key, value  in response.items():
        #       print 'hai',key,value
                if key=='VirtualMFADevices':
                        print '******************'
                        for i in value:
        #                       print '%%%%% i.keys %%%',i.keys(),' %%%%% i.values %%%%%',i.values()
                                for k,v in i.items():
        #                               print k,'###############',v
                                        if k=='SerialNumber':
                                                sno=v
#                                               print sno
                                        if k == 'User':
                                                for u,uv in v.items():
                                                        if u =='UserName' and uv == user_name:
                                                                serial_number=sno
                                                                return sno
print get_mfa_serial_number('user1')
mfa_disassociate('user1',get_mfa_serial_number('user1'))
