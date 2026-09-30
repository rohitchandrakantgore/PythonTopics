import json

from django.test import TestCase

from .models import Post


class PostApiTests(TestCase):
	collection_url = '/blog/api/posts/'

	def post_url(self, action, post_id):
		return f'/blog/api/posts/{action}/{post_id}/'

	def create_post(self, title='First post', content='Post content'):
		return Post.objects.create(title=title, content=content)

	def test_create_and_list_posts(self):
		response = self.client.post(
			f'{self.collection_url}create/',
			data=json.dumps({'title': 'Hello', 'content': 'World'}),
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json()['title'], 'Hello')
		self.assertEqual(Post.objects.count(), 1)

		response = self.client.get(self.collection_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 1)

	def test_retrieve_update_and_delete_post(self):
		post = self.create_post()
		detail_url = f'{self.collection_url}{post.id}/'

		response = self.client.get(detail_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['id'], post.id)

		response = self.client.put(
			self.post_url('update', post.id),
			data=json.dumps({'title': 'Updated', 'content': 'Replaced'}),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['title'], 'Updated')

		response = self.client.delete(self.post_url('delete', post.id))
		self.assertEqual(response.status_code, 204)
		self.assertFalse(Post.objects.filter(pk=post.id).exists())

	def test_missing_post_returns_404(self):
		response = self.client.get(f'{self.collection_url}999/')
		self.assertEqual(response.status_code, 404)

	def test_get_posts_rejects_post(self):
		response = self.client.post(self.collection_url)
		self.assertEqual(response.status_code, 405)
		self.assertEqual(response['Allow'], 'GET')
