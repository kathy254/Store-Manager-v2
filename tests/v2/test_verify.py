import unittest

from app.api.v2.models.verify import Verify

class TestVerification(unittest.TestCase):
	

	def setUp(self):
		self.obj = Verify()


	def tearDown(self):
		self.obj = None


	#test empty data
	def test_is_empty(self):
		test = self.obj.is_empty(['','dad'])
		self.assertTrue(test)


	#test if data is not emoty
	def test_not_empty(self):
		test = self.obj.is_empty(['fs','fs'])
		self.assertFalse(test)


	#test for white space
	def test_is_whitespace(self):
		test = self.obj.is_whitespace(['  ','d'])
		self.assertTrue(test)


	#test if there is no whitespace
	def test_not_whitespace(self):
		test = self.obj.is_whitespace(['d','df'])
		self.assertFalse(test)


	#test for correct product payload
	def test_is_product_payload(self):
		payload = {'productId': 1, 'Category': 'dresses', 'Product_name': 'Gucci dress', ' Quantity': 80, 'Price': 1500}
		test = self.obj.is_product_payload(payload)
		self.assertFalse(test)


    #test for incorrect payload
	def test_not_payload(self):
		payload = {'ProductId': 1, 'Category': 'dress', 'Quantity':80,'qwr':0}
		payload_2 = {'name':'Gucci','moq':3}
		payload_3 = {'name':'Gucci','Quantity': 50, 'Category':0,'we':0}
		test = self.obj.is_product_payload(payload)
		test_2 = self.obj.is_product_payload(payload_2)
		test_3 = self.obj.is_product_payload(payload_3)
		self.assertFalse(test)
		self.assertFalse(test_2)
		self.assertFalse(test_3)

if __name__ == '__main__':
    unittest.main()