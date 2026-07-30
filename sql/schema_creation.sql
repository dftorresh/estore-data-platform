USE EStoreERP;
GO

CREATE TABLE dbo.Customers
(
    customer_id        INT IDENTITY(1,1) PRIMARY KEY,
    first_name         NVARCHAR(100) NOT NULL,
    last_name          NVARCHAR(100) NOT NULL,
    email              NVARCHAR(255) NOT NULL UNIQUE,
    phone              NVARCHAR(50),
    registration_date  DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    status             VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.Addresses
(
    address_id         INT IDENTITY(1,1) PRIMARY KEY,
    customer_id        INT NOT NULL,
    address_type       VARCHAR(20) NOT NULL,
    address_line1      NVARCHAR(255) NOT NULL,
    address_line2      NVARCHAR(255),
    city               NVARCHAR(100) NOT NULL,
    state              NVARCHAR(100),
    country            NVARCHAR(100) NOT NULL,
    postal_code        NVARCHAR(20),
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT FK_Address_Customer
        FOREIGN KEY(customer_id)
        REFERENCES dbo.Customers(customer_id)
);

CREATE TABLE dbo.Categories
(
    category_id        INT IDENTITY(1,1) PRIMARY KEY,
    category_name      NVARCHAR(100) NOT NULL UNIQUE,
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.Suppliers
(
    supplier_id        INT IDENTITY(1,1) PRIMARY KEY,
    supplier_name      NVARCHAR(200) NOT NULL,
    contact_email      NVARCHAR(255),
    phone              NVARCHAR(50),
    country            NVARCHAR(100),
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.Products
(
    product_id         INT IDENTITY(1,1) PRIMARY KEY,
    category_id        INT NOT NULL,
    supplier_id        INT NOT NULL,
    product_name       NVARCHAR(255) NOT NULL,
    sku                NVARCHAR(100) NOT NULL UNIQUE,
    unit_price         DECIMAL(12,2) NOT NULL,
    active             BIT NOT NULL DEFAULT 1,
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    FOREIGN KEY(category_id)
        REFERENCES dbo.Categories(category_id),

    FOREIGN KEY(supplier_id)
        REFERENCES dbo.Suppliers(supplier_id)
);

CREATE TABLE dbo.Warehouses
(
    warehouse_id       INT IDENTITY(1,1) PRIMARY KEY,
    warehouse_name     NVARCHAR(100) NOT NULL,
    city               NVARCHAR(100),
    country            NVARCHAR(100),
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.Inventory
(
    inventory_id       INT IDENTITY(1,1) PRIMARY KEY,
    warehouse_id       INT NOT NULL,
    product_id         INT NOT NULL,
    quantity_available INT NOT NULL,
    quantity_reserved  INT NOT NULL DEFAULT 0,
    last_updated       DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT UQ_Inventory UNIQUE
    (
        warehouse_id,
        product_id
    ),

    FOREIGN KEY(warehouse_id)
        REFERENCES dbo.Warehouses(warehouse_id),

    FOREIGN KEY(product_id)
        REFERENCES dbo.Products(product_id)
);

CREATE TABLE dbo.Orders
(
    order_id           INT IDENTITY(1,1) PRIMARY KEY,
    customer_id        INT NOT NULL,
    order_date         DATETIME2 NOT NULL,
    order_status       VARCHAR(30) NOT NULL,
    total_amount       DECIMAL(12,2) NOT NULL,
    created_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    FOREIGN KEY(customer_id)
        REFERENCES dbo.Customers(customer_id)
);

CREATE TABLE dbo.OrderItems
(
    order_item_id      INT IDENTITY(1,1) PRIMARY KEY,
    order_id           INT NOT NULL,
    product_id         INT NOT NULL,
    quantity           INT NOT NULL,
    unit_price         DECIMAL(12,2) NOT NULL,
    line_total         DECIMAL(12,2) NOT NULL,

    FOREIGN KEY(order_id)
        REFERENCES dbo.Orders(order_id),

    FOREIGN KEY(product_id)
        REFERENCES dbo.Products(product_id)
);

CREATE TABLE dbo.Payments
(
    payment_id         INT IDENTITY(1,1) PRIMARY KEY,
    order_id           INT NOT NULL,
    payment_date       DATETIME2 NOT NULL,
    payment_method     VARCHAR(30) NOT NULL,
    amount             DECIMAL(12,2) NOT NULL,
    payment_status     VARCHAR(30) NOT NULL,

    FOREIGN KEY(order_id)
        REFERENCES dbo.Orders(order_id)
);

CREATE TABLE dbo.Shipments
(
    shipment_id        INT IDENTITY(1,1) PRIMARY KEY,
    order_id           INT NOT NULL,
    warehouse_id       INT NOT NULL,
    shipment_date      DATETIME2,
    delivery_date      DATETIME2,
    shipment_status    VARCHAR(30) NOT NULL,
    tracking_number    NVARCHAR(100),
    updated_at         DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    FOREIGN KEY(order_id)
        REFERENCES dbo.Orders(order_id),

    FOREIGN KEY(warehouse_id)
        REFERENCES dbo.Warehouses(warehouse_id)
);