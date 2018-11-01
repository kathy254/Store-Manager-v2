#library imports
from psycopg2.extras import RealDictCursor
import psycopg2

#local imports
from manage import DbSetup
from .verify import Verify
from .products_models import Products


class Sales(Verify):
	def __init__(self,items):
		self.items = items

	def check_sales_input(self):
		if self.is_sales_payload(self.items) is False:
			return {'result': 'Payload is invalid'},406
		elif self.items['quantity'] < 1:
			return {'result':'Product quantity cannot be less than 1'},406
		elif self.items['productId'] < 0:
			return {'result':'productId cannot be less than 0'},406
		else:
			return 1

	def add_sales_record(self):
		prodID = Products.get_product_by_id(self, productId)
		
		Sales.sales.append(items)
		return {
			'status': 'Success',
			'result': 'Sale added'}, 201