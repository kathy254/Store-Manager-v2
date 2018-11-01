from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Namespace, fields, Api

from ..utilities.auth import token_required
from ..models.user_models import Users


parser=reqparse.RequestParser()
parser.add_argument('first_name', help='This field cannot be blank')
parser.add_argument('last_name', help='This field cannot be blank')
parser.add_argument('email_address', help='This field cannot be blank')
parser.add_argument('role', help='This field cannot be blank')
parser.add_argument('password', help='This field cannot be blank')


store_users = Namespace('auth', description='Users endpoints')


mod_register = store_users.model('register store attendant', {
	'first_name':fields.String('attendant\'s first name'),
	'last_name': fields.String('attendants\'s last name'),
	'email_address': fields.String('attendant\'s email'),
	'password': fields.String('attendant\'s password'),
    'role': fields.String('attendant\'s role')
	})


@store_users.route('/register')
class RegisterStoreAttendant(Resource):
    @store_users.doc(security='apikey')
    @store_users.expect(mod_register)


    def post(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email_address = args['email_address']
        password = args['password']
        role = args['role']
        
        
        email_found = Users.get_user_by_email(email_address)
        
        if email_found == {'message': 'No records found'}:
            
            try:
                new_user = Users(first_name, last_name, email_address, password, role)
                return make_response(jsonify({
                    'status': 'success',
					'message': 'Account created. Please log in',
					'users': new_user
                }), 201)

            except Exception as e:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': str(e)
                }), 500)

        
        return make_response(jsonify({
			'status': 'failed',
			'message': 'Email address already exists. Please log in.'
		}), 500)

            
