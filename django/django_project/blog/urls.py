from django.urls import path

from . import views

urlpatterns = [
	path('api/posts/', views.get_posts, name='get-posts'),
	path('api/posts/<int:post_id>/', views.get_post, name='get-post'),
	path('api/posts/create/', views.create_post, name='create-post'),
	path('api/posts/update/<int:post_id>/', views.update_post, name='update-post'),
	path('api/posts/delete/<int:post_id>/', views.delete_post, name='delete-post'),
]
