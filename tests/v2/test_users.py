#imports from the library
import json

#imports from local folders
from .base_test import BaseTest
from app.api.v2.models.user_models import Users


registration_url = 'api/v2/auth/signup'
login_url = 'api/v2/auth/login'


class TestUsers(BaseTest):
    
    def test_register_users(self):
        with self.client():
            res = self.client().post(registration_url, data=json.dumps(dict(
                first_name = 'Store',
                last_name = 'Owner',
                email_address = 'store.admin@storemanager.com',
                role = 'Admin',
                password = 'admin254'
            )),
            content_type = 'application/json'
            )

            result = json.loads(res.data)
            self.assertEqual('Account created. Please log in', result['message'])
            self.assertEqual(res.status_code, 201)
            self.assertEqual('success', result['status'])
            self.assertTrue(res.content_type == 'application/json')


    def test_get_single_user_info(self):
        with self.client():
            res = self.client().post(registration_url, data=json.dumps(dict(
                first_name = 'Store',
                last_name = 'Owner',
                email_address = 'store.admin@storemanager.com',
                password = 'admin254',
                role = 'Admin'
            )),
            content_type = 'application/json'
            )

            self.assertEqual(res.status_code, 404)


    def test_register_existing_user(self):
        user = Users(
            first_name = 'Store',
            last_name = 'Owner',
            email_address = 'store.admin@storemanager.com',
            password = 'admin254',
            role = 'Admin'
        )

        with self.client():
            res = self.client().post(registration_url, data=json.dumps(dict(
                first_name = 'Store',
                last_name = 'Owner',
                email_address = 'store.admin@storemanager.com',
                password = 'admin254',
                role = 'Admin'
            )),
            content_type = 'application/json')

            result = json.loads(res.data)
            self.assertEqual('failed', result['status'])
            self.assertEqual('This email address already exists. Please login.', result['message'])
            self.assertTrue(res.content_type == 'application/json')
            self.assertEqual(res.status_code, 200)


    def test_login_function(self):
        with self.client():
            res = self.client().post(registration_url, data=json.dumps(dict(
                first_name = 'Store',
                last_name = 'Owner',
                email_address = 'store.admin@storemanager.com',
                password = 'admin254',
                role = 'Admin'
            )),
            content_type = 'application/json'
            )

            result = json.loads(res.data)
            self.assertEqual('Account created. Please log in.', result['message'])
            self.assertEqual('success', result['status'])
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')

            #login the user registered above
            res2 = self.client().post(login_url, data=json.dumps(dict(
                email_address = 'store.admin@storemanager.com',
                password = 'admin254'
            )),
            content_type = 'application/json'
            )

            result2 = json.loads(res2.data)
            self.assertEqual('You have logged in successfully.', result2['message'])
            self.assertEqual('success', result2['status'])
            self.assertTrue(res2.content_type == 'application/json')
            self.assertEqual(res2.status_code, 201)


    def test_encode_token(self):
        user = Users(
            first_name = 'Store',
            last_name = 'Owner',
            email_address = 'store.admin@storemanager.com',
            password = 'admin254',
            role = 'Admin'
        )

        token = user.encode_login_token(user.email_address, user.role)
        self.assertTrue(isinstance(token, bytes))


    def test_decode_token(self):
        user = Users(
            first_name = 'Store',
            last_name = 'Owner',
            email_address = 'store.admin@storemanager.com',
            password = 'admin254',
            role = 'Admin'
        )

        token = user.encode_login_token(user.email_address, user.role)
        self.assertTrue(isinstance(token, bytes))
        self.assertTrue(user.decode_auth_token(token)['role'] == 'Admin')