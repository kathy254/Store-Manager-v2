from flask import request, make_response, jsonify, Blueprint, json, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse, Api


from ..models.sales_models import Sales
from ..models.products_models import Products
from ..utilities.auth import token_required


parser = reqparse.RequestParser()
parser.add_argument('productId', help = 'This field cannot be blank', required = True)
parser.add_argument('Quantity', help = 'This field cannot be blank', required = True)
parser.add_argument('Price', help = 'This field cannot be blank', required = True)
parser.add_argument('sellerId', help = 'This field cannot be blank', required = True)


store_sales = Namespace('sales', description='Sales Endpoints')


mod = store_sales.model('sales model', {
        'productId': fields.Integer(description='Name of product sold'),
        'Quantity': fields.Integer(description='Quantity of product sold'),
        'Price': fields.Integer(description='Price of product sold'),
        'sellerId': fields.Integer(description='Id of the seller')
        })


@store_sales.route('')
class SaleRecord(Resource):
    @store_sales.expect(mod)
    @store_sales.doc(security='apikey')
    @token_required
    
    def post(self):
        #create a new sale record
        args = parser.parse_args()
        productId = args['productId']
        Quantity = args['Quantity']
        Price = args['Price']
        sellerId = args['sellerId']

        product = Products.get_product_by_id
        remaining_quantity = Quantity - product
        if product == 0:
            return make_response(jsonify({
                'message': 'This product is not available.'                
            }))
        if product >= remaining_quantity:
            new_sale = Sales(productId, Quantity, Price, sellerId)
            created_sale = new_sale.add_sales_record()
            return make_response(jsonify({
                'status': 'success',
                'message': 'Sale record created successfully',
                'sale': created_sale
            }), 201)

        return 'The quantity you are trying to sale is higher than the available quantity'

@store_sales.route('/<saleId>')
class GetSingleSale(Resource):
    @store_sales.doc(security='apikey')
    def get(self, saleId):
        single_sale = Sales.get_sale_by_sellerid
        if single_sale:
            return make_response(jsonify({
                'status': 'success',
                'message': 'Sale record',
                'sale': single_sale
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'Sale record not found'
        }), 404)

    