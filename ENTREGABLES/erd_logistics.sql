
CREATE TABLE client (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(100) UNIQUE NOT NULL,
    phone   VARCHAR(20),
    company VARCHAR(100)
);

CREATE TABLE product (
    id             SERIAL PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    logistics_type VARCHAR(50)
);

CREATE TABLE warehouse (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    location VARCHAR(150)
);

CREATE TABLE port (
    id               SERIAL PRIMARY KEY,
    name             VARCHAR(100) NOT NULL,
    is_international BOOLEAN DEFAULT FALSE,
    location         VARCHAR(150)
);

CREATE TABLE "user" (
    id         VARCHAR(50)  PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP    DEFAULT NOW()
);

CREATE TABLE shipment (
    id                SERIAL PRIMARY KEY,
    tracking_number   VARCHAR(50) UNIQUE NOT NULL,
    logistics_type    VARCHAR(50),
    product_quantity  INT          NOT NULL DEFAULT 1,
    registration_date TIMESTAMP    DEFAULT NOW(),
    delivery_date     TIMESTAMP,
    shipping_price    NUMERIC(12, 2),
    final_price       NUMERIC(12, 2),
    vehicle_plate     VARCHAR(20),
    fleet_number      VARCHAR(20),
    client_id         INT          NOT NULL REFERENCES client(id)    ON DELETE RESTRICT,
    product_id        INT          NOT NULL REFERENCES product(id)   ON DELETE RESTRICT,
    warehouse_id      INT          NOT NULL REFERENCES warehouse(id) ON DELETE RESTRICT,
    port_id           INT          NOT NULL REFERENCES port(id)      ON DELETE RESTRICT
);

CREATE INDEX idx_shipment_client    ON shipment(client_id);
CREATE INDEX idx_shipment_product   ON shipment(product_id);
CREATE INDEX idx_shipment_warehouse ON shipment(warehouse_id);
CREATE INDEX idx_shipment_port      ON shipment(port_id);
