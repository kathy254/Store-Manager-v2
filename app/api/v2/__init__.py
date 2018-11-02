from flask import Blueprint
from flask_restplus import Api

from .views.products import store_product
from .views.users import store_users
from .views.sales import store_sales

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


app_v2 = Blueprint('app_v2', __name__, url_prefix='/api/v2')
api_v2 = Api(app_v2, title = 'Store Manager API', version='2.0', description='Store Manager API version 2.0', authorizations='authorizations')


api_v2.add_namespace(store_product)
api_v2.add_namespace(store_users)
api_v2.add_namespace(store_sales)
