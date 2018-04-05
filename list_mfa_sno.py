import boto
from boto import iam
from flask import Flask, request
from json import dumps
from flask_restful import Resource, Api
#from flask.ext.jsonpify import jsonify
import boto3 
conn=iam.connect_to_region('us-west-2')
connection=iam.IAMConnection()
client=boto3.client('iam')
app=Flask(__name__)
api=Api(app)
user_name=''
serial_number=''
class Users(Resource):
	def get(self):
#		connect=connection.connect()
		users=connection.get_all_users()
		for user in users.users:
			mfaDevices=connection.get_all_mfa_devices(user.user_name)
			print mfaDevices,'##################'
		return users.users
class Getmfa(Resource):
	def put(self,user_name):
		paginator = client.get_paginator('list_virtual_mfa_devices')
		response = client.list_virtual_mfa_devices(AssignmentStatus='Any')
		sno=''
		print '$$$$$$$$$$$$$$$$$$$$$$$$',user_name
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
									print serial_number,sno
									return serial_number

		
		
api.add_resource(Users, '/users')
api.add_resource(Getmfa, '/getmfa/<string:user_name>')
if __name__ == '__main__':
	app.run(host='0.0.0.0')
