from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Namespace, reqparse, Resource, fields, Api

from ..utilities.auth import token_required
from ..models.products_models import Products

parser=reqparse.RequestParser()
parser.add_argument('productId', help='This field cannot be blank')
parser.add_argument('category', help='This field cannot be blank')
parser.add_argument('Product_name', help='This field cannot be blank')
parser.add_argument('Quantity', help='This field cannot be blank')
parser.add_argument('Price', help='This field cannot be blank')


store_product = Namespace('products', description='Products Endpoint')

mod = store_product.model('product model', {
    'productId': fields.Integer(description='Product ID'),
    'category': fields.String(descirption='Product category'),
    'Product_name': fields.String(description='Product Name'),
    'Quantity': fields.Integer(description='Product Quantity'),
    'Price': fields.Integer(description='Price of product'),
})


@store_product.route('')
class AllProducts(Resource):
    @token_required
    @store_product.doc(security='apikey')
    @store_product.expect(mod)


    def post(self):
        args = parser.parse_args()
        productId = args['productId']
        category = args['category']
        Product_name = args['Product_name']
        Quantity = args['Quantity']
        Price = args['Price']


        product = Products(productId, category, Product_name, Quantity, Price)
        new_product = product.add_product()
        return make_response(jsonify({
            'status': 'success',
            'message': 'Product added',
            'product': new_product
        }), 201)

