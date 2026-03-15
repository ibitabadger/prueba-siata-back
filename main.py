import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from controllers import (
    auth_controller,
    client_controller,
    port_controller,
    product_controller,
    shipment_controller,
    warehouse_controller,
)
from dependencies import require_auth_for_protected_paths

_cors_origins = [
    url.strip().rstrip("/")
    for url in [os.getenv("FRONTEND_URL", ""), os.getenv("FRONTEND_URL_PROD", "")]
    if url.strip()
]

app = FastAPI(
    title="API Logística",
    description="Prueba técnica gestión de envíos terrestres y marítimos",
    version="1.0.0",
    dependencies=[Depends(require_auth_for_protected_paths)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/api")
app.include_router(client_controller.router, prefix="/api")
app.include_router(product_controller.router, prefix="/api")
app.include_router(warehouse_controller.router, prefix="/api")
app.include_router(port_controller.router, prefix="/api")
app.include_router(shipment_controller.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "API Logística", "docs": "/docs"}
