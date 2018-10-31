import jwt

from passlib.hash import pbkdf2_sha256 as pbkdf2_sha256
import datetime

from instance.config import secret_key
from .verify import Verify
from manage import dbcommit

class Users():
    def __init__(self):
        self.db = dbcommit(self)
        

    def register_user(self, first_name, last_name, email_address, password, role):
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address,
            'password': password,
            'role': role
        }

        query = """INSERT INTO users(first_name, last_name, email_address, password, role) VALUES
                (%(first_name)s, %(last_name)s, %(email_address)s, %(password)s, %(role)s)"""

        cursor = self.db.cursor()
        cursor.execute(query, payload)
        self.db.commit()
        return payload


    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
        
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
        
        
    @staticmethod
    def encode_login_token(email_address, role):
        try:
            payload = {
				'exp': datetime.datetime.now() + datetime.timedelta(hours=24),
				'iat': datetime.datetime.now(),
				'sub': email_address,
				'role': role
			}
            
            token = jwt.encode(
				payload,
				secret_key,
				algorithm='HS256'
			)
            
            
            return token
            
        except Exception as e:
            return e
            
            
    @staticmethod
    def decode_auth_token(token):
        """Method to decode the auth token"""
        
        
        try:
            payload = jwt.decode(token, secret_key, options={'verify_iat': False})
            return payload
        except jwt.ExpiredSignatureError:
            return {'message': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token. Please log in again.'}
		
