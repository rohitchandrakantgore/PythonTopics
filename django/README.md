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
	|   |-- admin.py
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
| `settings.py` | Project configuration: installed apps, middleware, database, templates, time zone, static files, and security settings. |
| Project `urls.py` | Routes `/admin/` to Django admin and includes the blog URLs under `/blog/`. |
| `asgi.py` | ASGI application entry point, used by ASGI-compatible servers for asynchronous deployments. |
| `wsgi.py` | WSGI application entry point, used by traditional synchronous Python web servers. |
| `blog/models.py` | Defines the `Post` database model: title, content, creation time, and update time. |
| `blog/views.py` | Contains one function-based view for each blog API operation. |
| `blog/serializers.py` | Converts a `Post` model instance into a dictionary that can be returned as JSON. This project uses a small custom serializer, not Django REST Framework. |
| `blog/urls.py` | Maps the blog API paths to their individual views. |
| `blog/admin.py` | Registers `Post` so it can be managed through Django's built-in admin site. |
| `blog/migrations/` | Stores versioned database schema changes. `0001_initial.py` creates the `Post` table. |
| `blog/tests.py` | Tests the blog API behavior. |
| `store/models.py` | Defines the `Product` model with name, description, price, and timestamps. |
| `store/views.py` | Defines separate class-based views for listing, retrieving, creating, updating, and deleting products. |
| `store/serializers.py` | Converts a `Product` model instance to JSON-ready data. |
| `store/urls.py` | Maps store API paths to the class-based views. |
| `store/admin.py` | Registers `Product` in Django admin. |
| `store/migrations/` | Stores database schema changes for the store app. |
| `store/tests.py` | Tests the store API behavior. |
| `templates/` | HTML templates rendered by views, commonly stored inside an app. |
| `static/` | App-owned CSS, JavaScript, and image assets. |
| `forms.py` | Optional app module for form fields, validation, and model-backed forms. |

### Request flow

```text
HTTP request -> project urls.py -> blog/urls.py -> function view
                                                   |-> Post model/database
                                                   |-> serializers.py -> JSON response
```

Middleware runs around requests and responses. It can provide shared behavior such as sessions, authentication, security checks, and CSRF protection.

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

Store routes are mounted under `/store/`. Each product operation is handled by its own class-based view:

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
| `python manage.py migrate` | Apply unapplied migrations to the configured database. |
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

`makemigrations` creates versioned schema-change files; `migrate` applies them to the database. Commit migration files along with the model changes.

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
