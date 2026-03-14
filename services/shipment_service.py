from sqlalchemy.orm import Session, joinedload

from models import Shipment
from schemas import LogisticsType
from services.exceptions import DuplicateError


def _apply_discount(logistics_type: str, product_quantity: int, shipping_price: float) -> float:
    if product_quantity <= 10:
        return 0.0
    if logistics_type == LogisticsType.LAND.value:
        return shipping_price * 0.05
    if logistics_type == LogisticsType.MARITIME.value:
        return shipping_price * 0.03
    return 0.0


def list_shipments(db: Session) -> list:
    return (
        db.query(Shipment)
        .options(
            joinedload(Shipment.client),
            joinedload(Shipment.product),
        )
        .all()
    )


def get_shipment(shipment_id: int, db: Session):
    return (
        db.query(Shipment)
        .options(
            joinedload(Shipment.client),
            joinedload(Shipment.product),
        )
        .filter(Shipment.id == shipment_id)
        .first()
    )


def create_shipment(data: dict, db: Session) -> Shipment:
    if db.query(Shipment).filter(Shipment.tracking_number == data["tracking_number"]).first():
        raise DuplicateError("El número de guía ya existe")
    lt_val = data.pop("logistics_type")
    data["logistics_type"] = lt_val.value if hasattr(lt_val, "value") else lt_val
    lt = data["logistics_type"]
    discount = _apply_discount(lt, data["product_quantity"], data["shipping_price"])
    data["final_price"] = data["shipping_price"] - discount
    shipment = Shipment(**data)
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment


def update_shipment(shipment_id: int, data: dict, db: Session):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return None
    for k, v in data.items():
        setattr(shipment, k, v)
    discount = _apply_discount(
        shipment.logistics_type,
        shipment.product_quantity,
        shipment.shipping_price,
    )
    shipment.final_price = shipment.shipping_price - discount
    db.commit()
    db.refresh(shipment)
    return shipment


def delete_shipment(shipment_id: int, db: Session) -> bool:
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return False
    db.delete(shipment)
    db.commit()
    return True
