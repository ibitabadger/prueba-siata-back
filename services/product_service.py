from sqlalchemy.orm import Session

from models import Product


def _serialize_logistics_type(data: dict) -> dict:
    d = data.copy()
    if d.get("logistics_type") is not None and hasattr(d["logistics_type"], "value"):
        d["logistics_type"] = d["logistics_type"].value
    return d


def list_products(db: Session) -> list:
    return db.query(Product).all()


def get_product(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(data: dict, db: Session) -> Product:
    data = _serialize_logistics_type(data)
    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(product_id: int, data: dict, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    data = _serialize_logistics_type(data)
    for k, v in data.items():
        setattr(product, k, v)
    db.commit()
    db.refresh(product)
    return product


def delete_product(product_id: int, db: Session) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True
