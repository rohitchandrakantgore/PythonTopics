import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import ProductForm
from .models import Product
from .serializers import serialize_product


class ProductCatalogView(ListView):
	model = Product
	template_name = 'store/product_list.html'
	context_object_name = 'products'
	ordering = '-created_at'


class ProductCreatePageView(CreateView):
	form_class = ProductForm
	template_name = 'store/product_form.html'
	success_url = reverse_lazy('product-catalog')


class ProductListView(View):
	def get(self, request):
		products = [
			serialize_product(product)
			for product in Product.objects.order_by('-created_at')
		]
		return JsonResponse(products, safe=False)


class ProductDetailView(View):
	def get(self, request, product_id):
		product = get_object_or_404(Product, pk=product_id)
		return JsonResponse(serialize_product(product))


class ProductCreateView(View):
	def post(self, request):
		data = json.loads(request.body)
		product = Product.objects.create(
			name=data['name'],
			description=data['description'],
			price=data['price'],
		)
		return JsonResponse(serialize_product(product), status=201)


class ProductUpdateView(View):
	def put(self, request, product_id):
		product = get_object_or_404(Product, pk=product_id)
		data = json.loads(request.body)
		product.name = data['name']
		product.description = data['description']
		product.price = data['price']
		product.save()
		return JsonResponse(serialize_product(product))


class ProductDeleteView(View):
	def delete(self, request, product_id):
		product = get_object_or_404(Product, pk=product_id)
		product.delete()
		return HttpResponse(status=204)