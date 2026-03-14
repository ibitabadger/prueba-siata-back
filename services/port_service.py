from sqlalchemy.orm import Session

from models import Port


def list_ports(db: Session) -> list:
    return db.query(Port).all()


def get_port(port_id: int, db: Session):
    return db.query(Port).filter(Port.id == port_id).first()


def create_port(data: dict, db: Session) -> Port:
    port = Port(**data)
    db.add(port)
    db.commit()
    db.refresh(port)
    return port


def update_port(port_id: int, data: dict, db: Session):
    port = db.query(Port).filter(Port.id == port_id).first()
    if not port:
        return None
    for k, v in data.items():
        setattr(port, k, v)
    db.commit()
    db.refresh(port)
    return port


def delete_port(port_id: int, db: Session) -> bool:
    port = db.query(Port).filter(Port.id == port_id).first()
    if not port:
        return False
    db.delete(port)
    db.commit()
    return True
