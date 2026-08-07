CREATE INDEX IX_Customers_Email
ON Customers(email);

CREATE INDEX IX_Orders_Customer
ON Orders(customer_id);

CREATE INDEX IX_OrderItems_Order
ON OrderItems(order_id);

CREATE INDEX IX_OrderItems_Product
ON OrderItems(product_id);

CREATE INDEX IX_Inventory_Product
ON Inventory(product_id);

CREATE INDEX IX_Inventory_Warehouse
ON Inventory(warehouse_id);