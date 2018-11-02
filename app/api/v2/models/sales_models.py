#library imports
from psycopg2.extras import RealDictCursor
import psycopg2

#local imports
from manage import DbSetup, db_url
from .verify import Verify
from .products_models import Products


class Sales(Verify):
	def __init__(self, productId, Quantity, Price, sellerId):
		#initialize the constructor
		self.productId = productId
		self.Quantity = Quantity
		self.Price = Price
		self.sellerId = sellerId

	def check_sales_input(self):
		strings=self.productId, self.Quantity, self.Price, self.sellerId
		if self.is_sales_payload(strings) is False:
			return {'result': 'Payload is invalid'},406
		elif self.Quantity < 1:
			return {'result':'Product quantity cannot be less than 1'},406
		elif self.productId < 0:
			return {'result':'productId cannot be less than 0'},406
		else:
			return 1

	def add_sales_record(self):
		#this method adds a new sale record
		new_sale = dict(
			productId = self.productId,
			Quantity = self.Quantity,
			Price = self.Price,
			sellerId = self.sellerId
			)
		product = Products.get_product_by_id
		if product:
			current_quantity = product['quantity']
			print(current_quantity)
			if current_quantity > self.Quantity:
				remaining_quantity = current_quantity - self.Quantity
				query = """
							INSERT INTO sales(productId, Quantity, Price)
							VALUES (%s, %s, %s);
						"""
					
				update_query = """
									UPDATE products SET Quantity = %s 
									WHERE Product_name = %s
								"""
				con = psycopg2.connect(db_url)
				cur = con.cursor(cursor_factory=RealDictCursor)
				cur.execute(query, (self.productId, self.Quantity, self.Price, ))
				con.commit()

				con = psycopg2.connect(db_url)
				cur = con.cursor(cursor_factory = RealDictCursor)
				cur.execute(update_query, (remaining_quantity, self.productId))
				con.commit()
				return new_sale


	def get_all_records(self, saleId):
		query = """
					SELECT * FROM sales;
				"""

		con = psycopg2.connect(db_url)
		cur = con.cursor(cursor_factory = RealDictCursor)
		cur.execute(query, (saleId, ))
		sale = cur.fetchone()
		if sale:
			return sale
		return {'message': 'Sale record not found'}


	def get_sale_by_sellerid(self, sellerId):
		query = """
					SELECT * FROM sales
					WITH sellerId =%s;
				"""
			
		con = psycopg2.connect(db_url)
		cur = con.cursor(cursor_factory = RealDictCursor)
		cur.execute(query, (sellerId, ))
		sale_record = cur.fetchall()
		if sale_record:
			return sale_record
		return {'message': 'There are no sales records for this store attendant'}


	