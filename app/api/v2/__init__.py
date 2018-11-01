from flask import Blueprint
from flask_restplus import Api


from .views.users import store_users


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


app_v2 = Blueprint('app_v2', __name__, url_prefix='/api/v2')
api_v2 = Api(app_v2, title = 'Store Manager API', version='2.0', description='Store Manager API version 2.0', authorizations='authorizations')


api_v2.add_namespace(store_users)
