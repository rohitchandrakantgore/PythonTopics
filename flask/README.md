# Flask Learning App

This folder contains a small Flask application that exposes a JSON API for creating, listing, retrieving, updating, and deleting products. It uses SQLAlchemy 2 ORM with a local SQLite database.

## Components and request flow

```text
HTTP request -> Flask route -> validate JSON -> SQLAlchemy session -> SQLite
																			|                            |
																			+------ JSON response <-------+
```

| Component | Responsibility |
| --- | --- |
| `main.py` | Creates the Flask app, configures the database engine and session factory, defines the ORM model and API routes, and starts the development server. |
| `create_app()` | Application factory. It accepts an optional SQLAlchemy database URL, which allows tests to use a temporary database. |
| `Product` | SQLAlchemy ORM model mapped to the `products` table. Its columns are `id`, `name`, `description`, and `price`. |
| Engine | `create_engine()` opens the connection to SQLite. By default, the database file is `flask/products.db`. |
| Session | `sessionmaker()` creates sessions. A session loads ORM objects, adds or deletes rows, and persists changes with `commit()`. |
| `validate_product_data()` | Checks the JSON shape and required product fields before they are written to the database. |
| `serialize_product()` | Converts a `Product` object to JSON-ready values. The decimal price is returned as a string to preserve its decimal representation. |
| Flask routes | Match HTTP methods and URL paths to Python functions. `request` reads incoming JSON and `jsonify()` creates JSON responses. |
| `test_main.py` | Uses Python's built-in `unittest` and a temporary SQLite file to test CRUD behavior without changing the app database. |

The app uses SQLAlchemy directly; it does not use Flask-SQLAlchemy. `Base.metadata.create_all(engine)` creates tables that do not exist when the app starts. It does not update existing tables when model fields change; for a larger app, use a migration tool such as Alembic.

## Run the app

From the repository root, install the pinned project dependencies if needed, then start Flask:

```powershell
python -m pip install -r requirements.txt
Set-Location flask
python main.py
```

The development server is available at `http://127.0.0.1:5000/`. The root path returns `Hello, World!`; product APIs are under `/api/products`.

## Product API

All requests and responses use JSON, except a successful delete, which returns an empty `204` response.

| Method | Path | Purpose | Success status |
| --- | --- | --- | --- |
| `GET` | `/api/products` | List all products. | `200` |
| `GET` | `/api/products/<id>` | Retrieve one product. | `200` |
| `POST` | `/api/products` | Create a product. | `201` |
| `PUT` | `/api/products/<id>` | Replace a product's name, description, and price. | `200` |
| `DELETE` | `/api/products/<id>` | Delete a product. | `204` |

Create and update requests require all product fields:

```json
{
	"name": "Notebook",
	"description": "Ruled pages",
	"price": "4.50"
}
```

Names cannot be blank, descriptions must be strings, and prices must be non-negative numbers. Invalid request data returns `400`; a product ID that does not exist returns `404`.

## Database and ORM basics

The `Product` class defines a table and its columns. A SQLAlchemy session works with model objects and commits changes to SQLite:

```python
from sqlalchemy import select

# Read rows as Product objects.
products = session.scalars(select(Product).order_by(Product.name)).all()

# Add a new product.
product = Product(name="Notebook", description="Ruled pages", price="4.50")
session.add(product)
session.commit()

# Find one product by its primary key.
product = session.get(Product, 1)

# Save changed fields.
product.price = "5.00"
session.commit()

# Delete a product.
session.delete(product)
session.commit()
```

The API opens a session for each request and closes it when the request handler exits its `with` block. `add()` stages a new row, while `commit()` writes pending changes. `select()` describes a query; `session.scalars(...).all()` executes it and returns model instances.

## Run tests

From the repository root:

```powershell
python -m unittest discover -s flask -p "test_*.py" -v
```

The tests create a temporary SQLite database and dispose of its engine when finished. The normal app database is left untouched.
