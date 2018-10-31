import unittest
import json 

from app import create_app
from app.api.v2.models.user_models import Users


class TestValidData(unittest.TestCase):
    def setUp(self):
        self.test = create_app('testing').test_client()
        self.content_type = 'application/json'
        payload = {'first_name': 'myname', 'last_name': 'secondname', 'email_address': 'email@storemanager.com', 'password': 'admin', 'role': 'admin'}
        response = self.test.post('api/v1/auth/login',content_type=self.content_type, data=json.dumps(payload))
        data =json.loads(response.get_data().decode('UTF-8'))
        token = data['result']
        self.headers = {'X-API-KEY':'{}'.format(token)}
        
        
        def test_user_registration(self):
            payload = {
                'first_name': 'Mister',
                'last_name': 'User',
				'email_address': 'user@storemanager.com',
				'password': 'abcxyz',
                'role': 'attendant'
                }
            response = self.test.post('api/v1/auth/register',content_type=self.content_type,
                        data=json.dumps(payload),headers=self.headers)
            data =json.loads(response.get_data().decode('UTF-8'))
            self.assertEqual(response.status_code,201)

if __name__ == '__main__':
    unittest.main()

		