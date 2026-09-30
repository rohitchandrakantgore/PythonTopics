from django.urls import path

from .views import (
	ProductCreateView,
	ProductCreatePageView,
	ProductCatalogView,
	ProductDeleteView,
	ProductDetailView,
	ProductListView,
	ProductUpdateView,
)

urlpatterns = [
	path('', ProductCatalogView.as_view(), name='product-catalog'),
	path('products/new/', ProductCreatePageView.as_view(), name='product-create-page'),
	path('api/products/', ProductListView.as_view(), name='product-list'),
	path('api/products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
	path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
	path('api/products/update/<int:product_id>/', ProductUpdateView.as_view(), name='product-update'),
	path('api/products/delete/<int:product_id>/', ProductDeleteView.as_view(), name='product-delete'),
]