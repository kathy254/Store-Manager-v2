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


@store_users.route('/signup')
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


mod_login = store_users.model('users model', {
    'email_address': fields.String('Email address'),
    'password': fields.String('Password')
})


@store_users.route('/login')
class LoginUsers(Resource):
    @store_users.expect(mod_login)
    def post(self):
        args = parser.parse_args()
        email_address = args['email_address']
        password = args['password']


        try:
            current_user = Users.get_user_by_email(email_address)
            if current_user == {'message': 'No records found'}:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Email address not found. Please sign up.'
                }), 200)

            if current_user and password:
                role = current_user['role']
                email_address = current_user['email_address']
                token = Users.encode_login_token(email_address, role)
                if token:
                    return make_response(jsonify({
                        'status': 'success',
                        'message': 'You have logged in successfully.',
                        'token': token.decode()
                    }), 200)

            else:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Email address or password is invalid.'
                }), 400)

        except Exception as e:
            return make_response(jsonify({
                'status': 'failed',
                'message': str(e)
            }), 500)