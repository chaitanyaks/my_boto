import boto
from boto import iam
from flask import Flask, request
from json import dumps
from flask_restful import Resource, Api
#from flask.ext.jsonpify import jsonify

conn=iam.connect_to_region('us-west-2')
connection=iam.IAMConnection()
app=Flask(__name__)
api=Api(app)

class Users(Resource):
	def get(self):
#		connect=connection.connect()
		users=connection.get_all_users()
		for user in users.users:
			mfaDevices=connection.get_all_mfa_devices(user.user_name)
			print mfaDevices
		return users.users

api.add_resource(Users, '/users')
if __name__ == '__main__':
	app.run(host='0.0.0.0')
#print dir(users), type(users)
#print users.list_users_response.users
#for user in  users.users:
#	print user.user_name
#	print dir(user)
