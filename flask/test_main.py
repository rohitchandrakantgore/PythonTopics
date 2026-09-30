import json
import tempfile
import unittest
from pathlib import Path

from main import create_app


class ProductApiTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.temp_dir = tempfile.TemporaryDirectory()
		database_path = Path(cls.temp_dir.name) / 'test.db'
		cls.app = create_app(f'sqlite:///{database_path.as_posix()}')
		cls.app.config['TESTING'] = True

	@classmethod
	def tearDownClass(cls):
		cls.app.extensions['sqlalchemy_engine'].dispose()
		cls.temp_dir.cleanup()

	def setUp(self):
		self.client = self.app.test_client()

	def test_product_crud(self):
		response = self.client.post(
			'/api/products',
			data=json.dumps({
				'name': 'Notebook',
				'description': 'Ruled pages',
				'price': '4.50',
			}),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 201)
		product_id = response.json['id']

		response = self.client.get('/api/products')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json), 1)

		response = self.client.get(f'/api/products/{product_id}')
		self.assertEqual(response.json['name'], 'Notebook')

		response = self.client.put(
			f'/api/products/{product_id}',
			json={
				'name': 'Sketchbook',
				'description': 'Blank pages',
				'price': '6.25',
			},
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['name'], 'Sketchbook')

		response = self.client.delete(f'/api/products/{product_id}')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(self.client.get(f'/api/products/{product_id}').status_code, 404)

	def test_create_rejects_invalid_data(self):
		response = self.client.post(
			'/api/products',
			json={'name': '', 'description': 'Bad product', 'price': '-1'},
		)
		self.assertEqual(response.status_code, 400)
		self.assertIn('error', response.json)


if __name__ == '__main__':
	unittest.main()