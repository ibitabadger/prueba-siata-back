from sqlalchemy.orm import Session

from models import Client, Shipment
from services.exceptions import ConflictError


def list_clients(db: Session) -> list[Client]:
    return db.query(Client).all()


def get_client(client_id: int, db: Session) -> Client | None:
    return db.query(Client).filter(Client.id == client_id).first()


def create_client(data: dict, db: Session) -> Client:
    client = Client(**data)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(client_id: int, data: dict, db: Session) -> Client | None:
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None
    for k, v in data.items():
        setattr(client, k, v)
    db.commit()
    db.refresh(client)
    return client


def delete_client(client_id: int, db: Session) -> bool:
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return False
    if db.query(Shipment).filter(Shipment.client_id == client_id).first():
        raise ConflictError("No se puede eliminar el cliente porque tiene envíos asociados.")
    db.delete(client)
    db.commit()
    return True
