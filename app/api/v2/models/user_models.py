import jwt
import psycopg2

from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from instance.config import secret_key
from .verify import Verify
from manage import db_init

class Users():
    def __init__(self, first_name, last_name, email_address, password, role):
        self.db = db_init(self)
        

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


    def user_by_email_address(self, email_address):
        #query data from the users table
        cursor = self.db.cursor()
        cursor.execute("""SELECT email_address FROM users ORDER BY email_address""")
        row = cursor.fetchone()
        while row is not None:
            return row
