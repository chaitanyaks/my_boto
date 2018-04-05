from flask import Flask, request
from json import dumps
from flask_restful import Resource, Api
#from flask.ext.jsonpify import jsonify
import boto3 
client=boto3.client('iam')
app=Flask(__name__)
api=Api(app)
user_name=''
serial_number=''
iam=boto3.resource('iam')

class Getmfa(Resource):
	def get(self,user_name):
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
									print serial_number
									mfa_device = iam.MfaDevice(user_name,serial_number)
									response = mfa_device.disassociate()
									return "{0} has been disassociated with mfa device".format(user_name)
								else:
									return "{0} User has not associated with mfa device".format(user_name)
	
	def mfa_disassociate(user_name,serial_number):
		print user_name,serial_number
		mfa_device = iam.MfaDevice(user_name,serial_number)
		response = mfa_device.disassociate()
		return response
		
api.add_resource(Getmfa, '/getmfa/<string:user_name>')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
