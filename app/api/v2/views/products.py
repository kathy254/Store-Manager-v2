from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Namespace, reqparse, Resource, fields, Api

from ..utilities.auth import token_required, admin_required
from ..models.products_models import Products
from ..models.user_models import Users


store_product = Namespace('products', description='Products Endpoint')


parser=reqparse.RequestParser()
parser.add_argument('productId', help='This field cannot be blank')
parser.add_argument('category', help='This field cannot be blank')
parser.add_argument('Product_name', help='This field cannot be blank')
parser.add_argument('Quantity', help='This field cannot be blank')
parser.add_argument('Price', help='This field cannot be blank')



mod = store_product.model('product model', {
    'productId': fields.Integer(description='Product ID'),
    'category': fields.String(descirption='Product category'),
    'Product_name': fields.String(description='Product Name'),
    'Quantity': fields.Integer(description='Product Quantity'),
    'Price': fields.Integer(description='Price of product'),
})


@store_product.route('')
class AllProducts(Resource):
    @store_product.doc(security='apikey')
    @store_product.expect(mod)
    #admin token required to create a new product
    @admin_required


    def post(self):
        #this method adds a new product to the inventory
        args = parser.parse_args()
        productId = args['productId']
        category = args['category']
        Product_name = args['Product_name']
        Quantity = args['Quantity']
        Price = args['Price']

        check_products = Products.get_product_by_name(self, Product_name)
        if check_products:
            return make_response(jsonify({
                'message': 'This product already exists. Do you want to edit it?'
            }))
        
        product = Products(productId, category, Product_name, Quantity, Price)
        new_product = product.add_product()
        return make_response(jsonify({
            'status': 'success',
            'message': 'Product added successfully',
            'product': new_product
        }), 201)


@store_product.doc(security='apikey')
@token_required
def get(self):
    #this function gets all products in the inventory
    all_products=Products.get_all_products(self)
    if len(all_products)==0:
        return make_response(jsonify({
            'status': 'success',
            'message': 'There are no products in the inventory.',
            'product': all_products
        }), 200)
    return make_response(jsonify({
        'status': 'success',
        'message': 'Here are the products in the inventory.',
        'products': all_products
    }), 200)


@store_product.route('/<int:productId>')
class GetProductById(Resource):
    #this function gets a single product by its ID
    @store_product.doc(security='apikey')
    @token_required
    def get(self, productId):
        single_item = Products.get_product_by_id
        if single_item:
            return make_response(jsonify({
                'status': 'success',
                'message': 'Here is the product',
                'product': single_item
            }),200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'Product not found',            
        }), 404)


    @store_product.expect(mod)
    @store_product.doc(security='apikey')
    @admin_required
    def put(self, product_id):
        """ Create a new product """
        args = parser.parse_args()
        productId = args['productId']
        category = args['category']
        Product_name = args['Product_name']
        Quantity = args['Quantity']
        Price = args['Price']

        find_product = Products.get_product_by_name
        if find_product:
            return make_response(jsonify({
                'message': 'This product already exists. Do you want to edit it?'
            }))
        up_product = Products(productId, category, Product_name, Quantity, Price)
        updated_product = up_product.update_product(product_id)
        return make_response(jsonify({
            'status': 'ok',
            'message': 'product edited successfully',
            'product': updated_product
        }), 201)  


    
    @store_product.doc(security='apikey')
    @admin_required
    def delete(self, product_id):
        product_to_delete = Products.get_product_by_id
        if product_to_delete:
            Products.delete_product(self, product_id)
            return make_response(jsonify({
                'status': 'ok',
                'message': 'product deleted successfully'
}))