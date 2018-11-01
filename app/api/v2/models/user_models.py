#library imports
import jwt
import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
import psycopg2
from psycopg2.extras import RealDictCursor

#local imports
from .verify import Verify
from instance.config import secret_key
from manage import db_url


class Users(Verify):
    def __init__(self, first_name, last_name, email_address, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password
        self.role = role


    def check_user_input(self):
        strings = self.email_address, self.password
        payload = self.is_login_payload(strings)
        if payload is False:
            res = {'result': 'Payload is invalid'}, 406
        elif self.is_empty(strings):
            res = {'result': 'Data set is empty'}, 406
        elif self.is_whitespace(strings):
            res = {'result': 'Data set contains only whitespace'}, 406
        elif self.is_email(self.email_address) is True:
            res = {'result': 'Email address is invalid'}
        else:
            res = 1
        return res


    def register_new_user(self):
        new_user = dict(
            first_name = self.first_name,
            last_name = self.last_name,
            email_address = self.email_address,
            password = self.password,
            role = self.role
        )

        query = """
                    INSERT INTO users(first_name, last_name, email_address, password, role)
                    VALUES(%(first_name)s, %(last_name)s, %(email_address)s, %(password)s, %(role)s);
                """

        con = psycopg2.connect(db_url)
        cur = con.cursor(cursor_factory = RealDictCursor)
        cur.execute(query, new_user)
        con.commit()
        return new_user


    @staticmethod
    def get_user_by_email(email_address):
        #retrieve a user by email address
        query = """
                    SELECT * FROM users where email_address=%s;
                """

        con = psycopg2.connect(db_url)
        cur = con.cursor(cursor_factory = RealDictCursor)
        cur.execute(query, (email_address, ))
        user = cur.fetchone()
        if user:
            return user
        else:
            return {'message': 'No records found'}


    @staticmethod
    def get_all_users():
        query = """
                    SELECT * FROM users;
                """
        con = psycopg2.connect(db_url)
        cur = con.cursor(cursor_factory = RealDictCursor)
        cur.execute(query)
        user = cur.fetchall()
        if user:
            return user
        else:
            return {'message': 'No users found'}


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
        #This method decodes the authorization token
        try:
            payload = jwt.decode(token, secret_key, options={'verify_iat': False})
            return payload
        except jwt.ExpiredSignatureError:
            return {'message': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token. Please log in again.'}


