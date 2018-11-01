#library imports
import psycopg2

#local imports
from .base_test import BaseTest
from app.api.v2.models.products_models import Products


login_url = '/api/v2/auth/login'
registration_url = 'api/v2/auth/signup'
products_url = 'api/v2/products'

class TestProductsFunction(unittest.TestCase):
    #Data

    Product1 = {
        'productId': 1,
        'category': "Men's clothes",
        'Product_name': 'Tom Ford Suit',
        'Quantity': 30,
        'Price': 1000
    }


    Product2 = {
        'productId': 2,
        'category': 'Ladies dresses',
        'Product_name': 'Gucci dress',
        'Quantity': 100,
        'Price': 1000
    }

    Product3 = {
        'productId': 3,
        'category': 'Kids clothes',
        'Product name': 'Zara',
        'Quantity': 80,
        'Price': 800
    }


    def test_post_product(self):
        with self.client():
            res = self.client().post(registration_url, data=json.dumps(dict(
                
            )))
