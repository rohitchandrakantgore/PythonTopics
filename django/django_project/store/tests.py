import json

from django.test import TestCase

from .models import Product


class ProductApiTests(TestCase):
	collection_url = '/store/api/products/'

	def action_url(self, action, product_id):
		return f'{self.collection_url}{action}/{product_id}/'

	def create_product(self):
		return Product.objects.create(
			name='Notebook', description='Ruled pages', price='4.50'
		)

	def test_create_and_list_products(self):
		response = self.client.post(
			f'{self.collection_url}create/',
			data=json.dumps({
				'name': 'Pen',
				'description': 'Blue ink',
				'price': '2.25',
			}),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json()['name'], 'Pen')

		response = self.client.get(self.collection_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 1)

	def test_get_update_and_delete_product(self):
		product = self.create_product()
		response = self.client.get(f'{self.collection_url}{product.id}/')
		self.assertEqual(response.status_code, 200)

		response = self.client.put(
			self.action_url('update', product.id),
			data=json.dumps({
				'name': 'Pencil',
				'description': 'HB pencil',
				'price': '1.75',
			}),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['name'], 'Pencil')

		response = self.client.delete(self.action_url('delete', product.id))
		self.assertEqual(response.status_code, 204)
		self.assertFalse(Product.objects.filter(pk=product.id).exists())

	def test_missing_product_returns_404(self):
		response = self.client.get(f'{self.collection_url}999/')
		self.assertEqual(response.status_code, 404)