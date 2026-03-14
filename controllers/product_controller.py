from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models import User
from schemas import ProductCreate, ProductResponse, ProductUpdate
from services.product_service import (
    create_product,
    delete_product as delete_product_svc,
    get_product,
    list_products,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
@router.get("/", response_model=list[ProductResponse])
def list_products_endpoint(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_products(db)


@router.get("/{product_id:int}", response_model=ProductResponse)
def get_product_endpoint(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    product = get_product(product_id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(
    body: ProductCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return create_product(body.model_dump(), db)


@router.put("/{product_id:int}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    body: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = update_product(product_id, body.model_dump(exclude_unset=True), db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product


@router.delete("/{product_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    if not delete_product_svc(product_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
