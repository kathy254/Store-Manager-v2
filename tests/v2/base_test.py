"""
    this test file contains the common sets of tests 
    that are shared or reused by all other tests
"""


#imports from the library
import unittest
import psycopg2

#local imports
from instance.config import app_config
from app import create_app
from manage import DbSetup


registration_url = '/api/v2/auth/signup'
login_url = '/api/v2/auth/login'


class BaseTest(unittest.TestCase):
    #This class holds all similar test configurations
    database = DbSetup(config_name='testing')
    database.drop_tables()
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()

        with self.app_context:
            self.app_context.push


    def test_user_registration(self, first_name='Store', last_name='Owner', email_address='store.admin@storemanager.com', password='admin254', role='Admin'):
        registration_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address,
            'password': password,
            'role': role
        }

        return self.client().post(registration_url, data=registration_data)


    def test_user_login(self, email_address='store.admin@storemanager.com', password='admin254'):
        login_data = {
            'email_address': email_address,
            'password': password
            }

        return self.client().post(login_url, data=login_data)


    # def tearDown(self):
    #     #this method removes all test variables and clears the test database
    #     with self.app_context:
    #         self.app_context.pop()