from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name', 'description', 'price']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
			'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
		}