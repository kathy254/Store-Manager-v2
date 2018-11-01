#library imports
import psycopg2
from psycopg2.extras import RealDictCursor

#local imports
from manage import DbSetup, db_url
from .verify import Verify


class Products(Verify):
    def __init__(self, productId, category, Product_name, Quantity, Price):
        self.productId = productId
        self.category = category
        self.Product_name = Product_name
        self.Quantity = Quantity
        self.Price = Price
        
        
    def check_product_input(self):
        strings=self.productId, self.Quantity, self.Price
        payload = self.is_product_payload(strings)
        if payload is False:
            return {'result':'Payload is invalid'},406
        elif self.is_empty(strings) is True:
            return {'result':'Data set is empty'},406
        elif self.is_whitespace(strings) is True:
            return {'result':'data set contains only white space'},406
        elif self.Quantity < 1:
            return {'result':'Product quantity cannot be less than 1'},406
        elif self.Price < 1:
            return {'result':'Price cannot be less than 0'},406
        else:
            return 1
            
            
    def add_product(self):
        new_product = dict(
            productId = self.productId,
            category = self.category,
            Product_name = self.Product_name,
            Quantity = self.Quantity,
            Price = self.Price
        )

    
        query = """
                    INSERT INTO products(productId, category, Product_name, Quantity, Price)
                    VALUES (%(productId)s, %(category)s, %(Product_name)s, %(Quantity)s, %(Price)s)
                """

        con = psycopg2.connect(db_url)
        cur = con.cursor(cursor_factory = RealDictCursor)
        cur.execute(query, new_product)
        con.commit()
        return new_product
        
        
    def get_all_products(self):
        query = """
                    SELECT * FROM products
                """

        con = psycopg2.connect(db_url)
        cur = con.cursor()
        cur.execute(query)
        products = cur.fetchall()
        if products:
            return products
        return {'message': 'No products found'}
        
        
    def get_product_by_id(self, productId):
        query = """
                    SELECT * FROM products WHERE productId=%s
                """

        con = psycopg2.connect(db_url)
        cur = con.cursor(cursor_factory = RealDictCursor)
        cur.execute(query, (productId))
        product = cur.fetchone()
        if product:
            return product
        else:
            return {'message': 'Product not found'}