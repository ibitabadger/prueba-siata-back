# Prueba SIATA - EAFIT (Backend)

Backend desarrollado con **Python**, **FastAPI**, **SQLAlchemy**, **Alembic** y **PostgreSQL(Supabase)**.

## Requisitos previos

- **Python 3.11** (recomendado)

## Instalación

Desde la carpeta `backend` crear y activar un entorno virtual e instalar las  dependencias:

```bash
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

Agregar las variables de entorno a la raiz de la carpeta backend. 
Este archivo se comparte por correo.

## Migraciones de base de datos

Aplicar las migraciones de Alembic para crear/actualizar el esquema en la base de datos:

```bash
alembic upgrade head
```

## Ejecutar el servidor

Desde la carpeta `backend` (con el entorno virtual activo):

```bash
uvicorn main:app --reload
```

Por defecto, la API quedará disponible en `http://localhost:8000`.

## Entregables y documentación

En la carpeta `ENTREGABLES` se encuentra la documentación formal del proyecto:

- Subcarpeta **`DIAGRAMA E-R`**: diagrama entidad-relación en formato `.drawio` y como imagen `.png`.
- Archivo **`erd_logistics.sql`**: esquema de la base de datos.
- Archivo **`doc.pdf`** incluyendo:
  - Definición de buenas prácticas.
  - Justificación de tecnologías y patrones de diseño.
  - Artefactos de despliegue de la solución,
  - Documentación completa del proyecto.

## Autora

**Andrea Sánchez**