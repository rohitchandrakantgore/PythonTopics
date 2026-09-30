def serialize_post(post):
	return {
		'id': post.id,
		'title': post.title,
		'content': post.content,
		'created_at': post.created_at.isoformat(),
		'updated_at': post.updated_at.isoformat(),
	}