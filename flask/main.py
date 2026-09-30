from decimal import Decimal, InvalidOperation
from pathlib import Path

from flask import Flask, jsonify, request
from sqlalchemy import Integer, Numeric, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)


def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': f'{product.price:.2f}',
    }


def validate_product_data(data):
    if not isinstance(data, dict):
        return None, 'Request body must be a JSON object.'

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not isinstance(name, str) or not name.strip():
        return None, 'Name is required.'
    if not isinstance(description, str):
        return None, 'Description is required.'

    try:
        price = Decimal(str(price))
        if not price.is_finite() or price < 0:
            return None, 'Price must be a non-negative number.'
    except (InvalidOperation, ValueError):
        return None, 'Price must be a non-negative number.'

    return {
        'name': name.strip(),
        'description': description,
        'price': price,
    }, None


def create_app(database_url=None):
    app = Flask(__name__)
    database_url = database_url or f"sqlite:///{Path(__file__).with_name('products.db').as_posix()}"
    connect_args = {'check_same_thread': False} if database_url.startswith('sqlite:') else {}
    engine = create_engine(database_url, connect_args=connect_args)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    app.extensions['sqlalchemy_engine'] = engine

    @app.get('/')
    def home():
        return 'Hello, World!'

    @app.get('/api/products')
    def get_products():
        with Session() as session:
            products = session.scalars(select(Product).order_by(Product.id)).all()
            return jsonify([serialize_product(product) for product in products])

    @app.get('/api/products/<int:product_id>')
    def get_product(product_id):
        with Session() as session:
            product = session.get(Product, product_id)
            if product is None:
                return jsonify({'error': 'Product not found.'}), 404
            return jsonify(serialize_product(product))

    @app.post('/api/products')
    def create_product():
        data, error = validate_product_data(request.get_json(silent=True))
        if error:
            return jsonify({'error': error}), 400

        with Session() as session:
            product = Product(**data)
            session.add(product)
            session.commit()
            return jsonify(serialize_product(product)), 201

    @app.put('/api/products/<int:product_id>')
    def update_product(product_id):
        data, error = validate_product_data(request.get_json(silent=True))
        if error:
            return jsonify({'error': error}), 400

        with Session() as session:
            product = session.get(Product, product_id)
            if product is None:
                return jsonify({'error': 'Product not found.'}), 404

            product.name = data['name']
            product.description = data['description']
            product.price = data['price']
            session.commit()
            return jsonify(serialize_product(product))

    @app.delete('/api/products/<int:product_id>')
    def delete_product(product_id):
        with Session() as session:
            product = session.get(Product, product_id)
            if product is None:
                return jsonify({'error': 'Product not found.'}), 404

            session.delete(product)
            session.commit()
            return '', 204

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)