# Django Learning Notes

This folder contains a starter Django project at `django_project/`. Django is a Python web framework for building web applications. It includes URL routing, an object-relational mapper (ORM), templating, forms, authentication, an admin site, and other common web features.

## Project Layout

The current project was created with `django-admin startproject` and uses SQLite by default.

```text
django/
|-- README.md
`-- django_project/
	|-- blog/
	|   |-- migrations/
	|   |   `-- 0001_initial.py
	|   |-- admin.py
	|   |-- models.py
	|   |-- serializers.py
	|   |-- tests.py
	|   |-- urls.py
	|   `-- views.py
	|-- store/
	|   |-- migrations/
	|   |-- static/store/
	|   |   `-- store.css
	|   |-- templates/store/
	|   |   |-- product_form.html
	|   |   `-- product_list.html
	|   |-- admin.py
	|   |-- forms.py
	|   |-- models.py
	|   |-- serializers.py
	|   |-- tests.py
	|   |-- urls.py
	|   `-- views.py
	|-- django_project/
	|   |-- asgi.py
	|   |-- settings.py
	|   |-- urls.py
	|   `-- wsgi.py
	`-- manage.py
```

### Project and app

- A **project** is the configuration and URL entry point for a complete website. This project package is `django_project`.
- An **app** is a reusable feature area inside a project, such as `blog`, `store`, or `accounts`. Apps contain the code for a particular domain and are added to `INSTALLED_APPS` in `settings.py`.
- A project can contain multiple apps, and an app can be reused by more than one project.

### Important files and components

| Component | Purpose |
| --- | --- |
| `manage.py` | Runs Django management commands for this project. It sets the settings module and passes commands to Django. |
| `settings.py` | Project configuration: installed apps, middleware, database, templates, time zone, static files, and security settings. Add each app to `INSTALLED_APPS` so Django can load its models, migrations, and admin configuration. |
| Project `urls.py` | Main URL router. Sends `/admin/` to Django admin and includes app URL files under `/blog/` and `/store/`. |
| `asgi.py` | ASGI application entry point, used by ASGI-compatible servers for asynchronous deployments. |
| `wsgi.py` | WSGI application entry point, used by traditional synchronous Python web servers. |
| `blog/models.py`, `store/models.py` | Define database models (`Post` and `Product`). Each model class describes a table, and each field describes a column. |
| `blog/views.py` | Contains function-based request handlers. Each function handles one API operation and returns an HTTP response. |
| `store/views.py` | Contains class-based views. Each class handles one product operation; methods such as `get()`, `post()`, `put()`, and `delete()` handle HTTP methods. |
| `blog/serializers.py`, `store/serializers.py` | Convert model instances to dictionaries that `JsonResponse` can return as JSON. These are small custom serializers, not Django REST Framework serializers. |
| `blog/urls.py`, `store/urls.py` | Map app URL paths to views. Class-based views are connected with `.as_view()`. |
| `blog/admin.py` | Registers `Post` so it can be managed through Django's built-in admin site. |
| `blog/migrations/` | Stores versioned database schema changes. `0001_initial.py` creates the `Post` table. |
| `blog/tests.py` | Tests the blog API behavior. |
| `store/models.py` | Defines the `Product` model with name, description, price, and timestamps. |
| `store/views.py` | Defines class-based views for the product catalog page and for listing, retrieving, creating, updating, and deleting products. |
| `store/forms.py` | Defines `ProductForm`, a `ModelForm` that validates product form input and creates a `Product`. |
| `store/serializers.py` | Converts a `Product` model instance to JSON-ready data. |
| `store/urls.py` | Maps store API paths to the class-based views. |
| `store/templates/store/` | Contains the product catalog and add-product HTML templates. |
| `store/static/store/` | Contains the store page stylesheet. |
| `store/admin.py` | Registers `Product` in Django admin. |
| `store/migrations/` | Stores database schema changes for the store app. |
| `store/tests.py` | Tests the store API behavior. |
| `templates/` | HTML templates rendered by views, commonly stored inside an app. |
| `static/` | App-owned CSS, JavaScript, and image assets. |
| `forms.py` | Optional app module for form fields, validation, and model-backed forms. |

### Store components

The store app uses these pieces together to display and create products:

| Component | What it does in this app |
| --- | --- |
| Model (`store/models.py`) | `Product` defines the fields saved in the database: name, description, price, and timestamps. Django's ORM reads and writes these records. |
| Migration (`store/migrations/`) | Records database schema changes for the model. `migrate` applies those changes to SQLite. |
| View (`store/views.py`) | `ProductCatalogView` gets products for the catalog template. `ProductCreatePageView` uses Django's `CreateView` to validate and save the HTML form. API views receive JSON requests and call the ORM. |
| Form (`store/forms.py`) | `ProductForm` is a `ModelForm`: it builds fields from `Product`, validates submitted values on the server, and saves a valid model instance. |
| URL configuration (`store/urls.py`) | Connects paths such as `/store/` and `/store/api/products/create/` to their views. `.as_view()` turns a class-based view into a URL handler. |
| Serializer (`store/serializers.py`) | `serialize_product()` turns a model instance into a Python dictionary for JSON responses. The decimal price is converted to a string so it can be encoded safely. It is a small project function, not a Django REST Framework serializer. |
| Template (`store/templates/store/`) | Django renders `product_list.html` and `product_form.html` as HTML. The views provide data and templates define its presentation. |
| Static CSS (`store/static/store/store.css`) | Styles the catalog and form. `{% load static %}` and `{% static 'store/store.css' %}` generate the correct stylesheet URL. |
| Static CSS (`store/static/store/store.css`) | Styles the catalog and add-product form. |

### Django templates

This project uses Django's built-in template language (DTL), not Jinja2. DTL uses double braces to display values and `{% ... %}` tags to load static files, build URLs, and control template flow. For example:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'store/store.css' %}">
<h1>{{ product.name }}</h1>
```

The catalog template loops over products supplied by `ProductCatalogView`. The form template includes `{% csrf_token %}` so its JavaScript can submit a CSRF-protected request to the product API. Django templates render on the server; CSS and JavaScript are static assets served separately during development.

### Request flow

```text
HTTP request -> project urls.py -> app urls.py -> view
												|-> model/ORM -> database
												|-> serializer -> JSON response
```

Middleware runs around requests and responses. It can provide shared behavior such as sessions, authentication, security checks, and CSRF protection.

### Django ORM basics

Django's ORM lets Python code read and change database records through model classes. `Post.objects` and `Product.objects` are model managers; they create querysets or return model instances. Run `python manage.py shell` from the project directory, then try:

```python
from blog.models import Post
from store.models import Product

# Create a row and save it immediately.
post = Post.objects.create(title="ORM basics", content="A first post")

# Build a query for matching rows. Field lookups can be chained.
posts = Post.objects.filter(title__icontains="orm").order_by("-created_at")

# Get one row by primary key. This raises Post.DoesNotExist if there is no match.
post = Post.objects.get(pk=post.id)

# Change one model instance and save it.
post.title = "Updated title"
post.save()

# Update matching rows directly in the database.
Product.objects.filter(price__lt=5).update(description="Under five dollars")

# Delete one matching row; delete() can also be called on a model instance.
Post.objects.filter(pk=post.id).delete()
```

Common queryset methods:

| Method | Use |
| --- | --- |
| `all()` | Return a queryset containing all rows, for example `Product.objects.all()`. |
| `filter(**lookups)` | Return rows matching conditions, for example `Product.objects.filter(price__gte=10)`. |
| `exclude(**lookups)` | Return rows that do not match conditions. |
| `get(**lookups)` | Return one matching object. It raises `DoesNotExist` for no match and `MultipleObjectsReturned` for more than one. |
| `order_by(field)` | Sort results; prefix a field with `-` for descending order, such as `order_by('-created_at')`. |
| `create(**fields)` | Create and save a row in one call. |
| `update(**fields)` | Update every row in a queryset with one database query. It does not call each object's `save()` method or update `auto_now` fields. |
| `delete()` | Delete all rows in a queryset and return deletion counts. |
| `count()` / `exists()` | Check how many rows match, or whether any rows match, without loading all model objects. |

For an individual model instance, `save()` writes its current field values, and `delete()` removes that row. Since `updated_at` uses `auto_now=True`, use `instance.save()` when you want that timestamp to update automatically; queryset `update()` bypasses it. Querysets are lazy: chaining `filter()` and `order_by()` builds a query, and the database is generally queried when the results are used.

## Getting Started

Run commands from the directory containing `manage.py`:

```powershell
cd django\django_project
```

Activate the Python environment you use for this repository. If Django is not installed in it, install Django:

```powershell
python -m pip install Django
```

Check the setup, apply the database migrations, and start the local development server:

```powershell
python manage.py check
python manage.py migrate
python manage.py runserver
```

The server runs at `http://127.0.0.1:8000/`. The project does not define a home page at `/`; use the blog API paths below or open the admin site at `http://127.0.0.1:8000/admin/`.

### Blog API

The blog routes are mounted under `/blog/`. Each operation has its own function view:

| Method | Path | Use |
| --- | --- | --- |
| `GET` | `/blog/api/posts/` | Get all posts. |
| `GET` | `/blog/api/posts/<id>/` | Get one post by its database ID. |
| `POST` | `/blog/api/posts/create/` | Create a post. |
| `PUT` | `/blog/api/posts/update/<id>/` | Replace a post's title and content. |
| `DELETE` | `/blog/api/posts/delete/<id>/` | Delete a post. |

Create and update requests send JSON with both fields:

```json
{
	"title": "My first post",
	"content": "This is the post content."
}
```

The API response includes the post ID, title, content, and timestamps. A missing post returns `404`. The project has Django's CSRF middleware enabled, so clients making `POST`, `PUT`, or `DELETE` requests must provide a valid CSRF token.

### Store API

The product catalog is at `/store/`, and the add-product form is at `/store/products/new/`. The form uses `ProductForm` and submits normally to `ProductCreatePageView`, which validates and saves it on the server. The JSON API remains available separately under `/store/api/`:

| Method | Path | Use |
| --- | --- | --- |
| `GET` | `/store/api/products/` | Get all products. |
| `GET` | `/store/api/products/<id>/` | Get one product by its database ID. |
| `POST` | `/store/api/products/create/` | Create a product. |
| `PUT` | `/store/api/products/update/<id>/` | Replace a product's name, description, and price. |
| `DELETE` | `/store/api/products/delete/<id>/` | Delete a product. |

Create and update requests send JSON with all product fields:

```json
{
	"name": "Notebook",
	"description": "Ruled pages",
	"price": "4.50"
}
```

The API response includes the product ID, fields, and timestamps. Store API write requests also require a valid CSRF token.

### Admin interface

`Post` and `Product` are registered in their apps' `admin.py` files, so staff users can manage both through Django admin:

1. Apply migrations with `python manage.py migrate`.
2. Create an admin account with `python manage.py createsuperuser` and follow the prompts.
3. Start the server with `python manage.py runserver`.
4. Open `http://127.0.0.1:8000/admin/`, sign in, and select **Posts** or **Products**.

The admin site and APIs use the same database. Posts and products created in admin appear in their APIs, and records created through the APIs appear in admin.

## Common Django Commands

Run these from `django/django_project`, beside `manage.py`.

| Command | Use |
| --- | --- |
| `python manage.py help` | List available commands. Add a command name, such as `help startapp`, for command-specific help. |
| `python manage.py check` | Find common project configuration problems. |
| `python manage.py runserver` | Start Django's local development server. Use `runserver 8080` to choose another port. |
| `python manage.py startapp blog` | Create a new app named `blog` in the current directory. |
| `python manage.py makemigrations` | Create migration files for detected model changes. Use `makemigrations blog` to target one app. |
| `python manage.py migrate` | Apply unapplied migrations to the configured database, creating or altering tables to match models. |
| `python manage.py showmigrations` | Show migrations and whether each has been applied. |
| `python manage.py sqlmigrate blog 0001` | Show the SQL Django would run for a migration. Replace the app and migration names as needed. |
| `python manage.py createsuperuser` | Create a privileged account for the Django admin site. |
| `python manage.py changepassword username` | Change a user's password. |
| `python manage.py shell` | Open a Python shell with the Django project configured. |
| `python manage.py test` | Run the project's automated tests. Use `test blog` to run one app's tests. |
| `python manage.py collectstatic` | Gather static assets for deployment when static-file settings are configured. |

Typical model-change workflow:

```powershell
python manage.py makemigrations blog
python manage.py migrate
```

`makemigrations` compares the current models with recorded migration state and creates versioned schema-change files; it does not change the database. `migrate` applies those files to the database. Commit migration files with their model changes.

## Creating an App

For example, create a `blog` app from the directory containing `manage.py`:

```powershell
python manage.py startapp blog
```

Then add `'blog'` to `INSTALLED_APPS` in `django_project/settings.py`. A typical app adds models in `blog/models.py`, views in `blog/views.py`, and URL patterns in `blog/urls.py`. Include the app's URL patterns from the project's `django_project/urls.py` using `include()`.

## Development and Security Notes

- `runserver` is for local development, not production hosting.
- Keep `DEBUG = True` only for local development. Production deployments need `DEBUG = False`, appropriate `ALLOWED_HOSTS`, and a securely managed `SECRET_KEY`.
- Do not commit real credentials or production secrets to source control.
- After changing models, create and apply migrations before relying on the updated database schema.
