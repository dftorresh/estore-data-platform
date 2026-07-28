import random
from datetime import datetime
import uuid

def get_random_warehouse(db):

    warehouses = db.fetch_all(
        """
        SELECT warehouse_id
        FROM Warehouses
        """
    )

    return random.choice(warehouses)["warehouse_id"]


SHIPMENT_STATUS = [
    "CREATED",
    "SHIPPED"
]

def create_shipment(
    db,
    order_id
):

    db.execute(
        """
        INSERT INTO Shipments
        (
            order_id,
            warehouse_id,
            shipment_date,
            shipment_status,
            tracking_number
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
        """,
        (
            order_id,
            get_random_warehouse(db),
            datetime.utcnow(),
            random.choice(SHIPMENT_STATUS),
            str(uuid.uuid4())[:12].upper()
        )
    )


def reduce_inventory(
    db,
    order_id
):

    items = db.fetch_all(
        """
        SELECT
            oi.product_id,
            oi.quantity,
            s.warehouse_id
        FROM OrderItems oi
        INNER JOIN Shipments s
            ON oi.order_id = s.order_id
        WHERE oi.order_id = %s
        """,
        (order_id,)
    )

    for item in items:

        db.execute(
            """
            UPDATE Inventory
            SET
                quantity_available =
                    quantity_available - %s,
                last_updated = GETUTCDATE()
            WHERE warehouse_id = %s
              AND product_id = %s
            """,
            (
                item["quantity"],
                item["warehouse_id"],
                item["product_id"]
            )
        )