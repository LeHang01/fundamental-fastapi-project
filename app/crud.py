from sqlalchemy.orm import Session
from app.model import Product
from app.schema import ProductSchema


def get_product(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductSchema):
    _product = Product(title=product.title, description=product.description)
    db.add(_product)
    db.commit()
    db.refresh(_product)
    return _product


def remove_product(db: Session, product_id: int):
    _product = get_product_by_id(db=db, product_id=product_id)
    db.delete(_product)
    db.commit()


def update_product(db: Session, product_id: int, title: str, description: str):
    _product = get_product_by_id(db=db, product_id=product_id)

    _product.title = title
    _product.description = description

    db.commit()
    db.refresh(_product)
    return _product