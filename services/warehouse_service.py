from sqlalchemy.orm import Session

from models import Shipment, Warehouse


def list_warehouses(db: Session) -> list:
    return db.query(Warehouse).all()


def get_warehouse(warehouse_id: int, db: Session):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def create_warehouse(data: dict, db: Session) -> Warehouse:
    warehouse = Warehouse(**data)
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def update_warehouse(warehouse_id: int, data: dict, db: Session):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        return None
    for k, v in data.items():
        setattr(warehouse, k, v)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def delete_warehouse(warehouse_id: int, db: Session) -> bool:
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        return False
    db.query(Shipment).filter(Shipment.warehouse_id == warehouse_id).update({Shipment.warehouse_id: None})
    db.delete(warehouse)
    db.commit()
    return True
