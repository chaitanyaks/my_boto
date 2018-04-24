from flask import Flask, request
from flask_restful import Resource, Api
from botocore.exceptions import ClientError
import boto3

client = boto3.client('iam')
app = Flask(__name__)
api = Api(app)
user_name = ''
serial_number = ''

class Getmfa(Resource):
	def get(self,user_name):
		try:
			response = client.list_mfa_devices(UserName = user_name)
			if len(response['MFADevices']):
				serial_number = response['MFADevices'][0]['SerialNumber']
				user_name = response['MFADevices'][0]['UserName']
				if serial_number and user_name:
					print "{0}'s serial number is {1}".format(user_name, serial_number)
					deactivate_response = client.deactivate_mfa_device(UserName = user_name, SerialNumber = serial_number)
					return "{0} has been disassociated with mfa device".format(user_name)
			else:
				return "{0} is not associated with mfa device...!".format(user_name)
		except ClientError as e:
			if e.response['Error']['Code'] == 'NoSuchEntity':
				return 'The user with name {0} cannot be found.'.format(user_name)
			else:
				# TODO: handle other errors there
				return 'Unexpected error {0}'.format(e)
api.add_resource(Getmfa, '/getmfa/<string:user_name>')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
			
