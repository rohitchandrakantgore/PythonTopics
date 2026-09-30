def serialize_product(product):
	return {
		'id': product.id,
		'name': product.name,
		'description': product.description,
		'price': str(product.price),
		'created_at': product.created_at.isoformat(),
		'updated_at': product.updated_at.isoformat(),
	}