import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Post
from .serializers import serialize_post


@require_GET
def get_posts(request):
	data = [serialize_post(post) for post in Post.objects.order_by('-created_at')]
	return JsonResponse(data, safe=False)


@require_GET
def get_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return JsonResponse(serialize_post(post))


@require_POST
def create_post(request):
	data = json.loads(request.body)
	post = Post.objects.create(title=data['title'], content=data['content'])
	return JsonResponse(serialize_post(post), status=201)


@require_http_methods(['PUT'])
def update_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	data = json.loads(request.body)
	post.title = data['title']
	post.content = data['content']
	post.save()
	return JsonResponse(serialize_post(post))


@require_http_methods(['DELETE'])
def delete_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	post.delete()
	return HttpResponse(status=204)
