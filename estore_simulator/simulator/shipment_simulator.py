import uuid
import random
from datetime import datetime
from config_simulation import SIMULATION


SHIPMENT_STATUSES = {
    "CREATED": "CREATED",
    "READY_TO_SHIP": "READY_TO_SHIP",
    "SHIPPED": "SHIPPED",
    "IN_TRANSIT": "IN_TRANSIT",
    "DELIVERED": "DELIVERED"
}

NEXT_STATUS = {
    SHIPMENT_STATUSES["CREATED"]: SHIPMENT_STATUSES["READY_TO_SHIP"],
    SHIPMENT_STATUSES["READY_TO_SHIP"]: SHIPMENT_STATUSES["SHIPPED"],
    SHIPMENT_STATUSES["SHIPPED"]: SHIPMENT_STATUSES["IN_TRANSIT"],
    SHIPMENT_STATUSES["IN_TRANSIT"]: SHIPMENT_STATUSES["DELIVERED"]
}


def get_random_warehouse(db):

    warehouses = db.fetch_all(
        """
        SELECT warehouse_id
        FROM Warehouses
        """
    )

    return random.choice(warehouses)["warehouse_id"]


def create_shipment(
    db,
    order_id
):
    
    current_datetime =  datetime.utcnow()

    db.execute(
        """
        INSERT INTO Shipments
        (
            order_id,
            warehouse_id,
            shipment_date,
            shipment_status,
            tracking_number,
            updated_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
        """,
        (
            order_id,
            get_random_warehouse(db),
            current_datetime,
            SHIPMENT_STATUSES["CREATED"],
            str(uuid.uuid4())[:12].upper(),
            current_datetime
        )
    )


def update_shipments(db):

    shipments = db.fetch_all(
        """
        SELECT
            shipment_id,
            order_id,
            shipment_status
        FROM Shipments
        WHERE shipment_status <> 'DELIVERED'
        """
    )

    total = min(
        len(shipments),
        random.randint(
            *SIMULATION["shipments_to_process_per_day"]
        )
    )

    shipments = random.sample(shipments, total)
    total_shipments_updated = len(shipments)

    for shipment in shipments:

        # Only ~70% advance during a simulation run
        if random.random() > 0.70:
            total_shipments_updated -= 1
            continue

        current_status = shipment["shipment_status"]
        next_status = NEXT_STATUS[current_status]

        db.execute(
            """
            UPDATE Shipments
            SET
                shipment_status = %s,
                updated_at = GETUTCDATE()
            WHERE shipment_id = %s
            """,
            (
                next_status,
                shipment["shipment_id"]
            )
        )

        db.execute(
            """
            UPDATE Orders
            SET
                order_status = %s,
                updated_at = GETUTCDATE()
            WHERE order_id = %s
            """,
            (
                next_status,
                shipment["order_id"]
            )
        )

        if next_status == SHIPMENT_STATUSES["SHIPPED"]:

            reduce_inventory(
                db,
                shipment["order_id"]
            )

    print(f"Shipments and orders updated: {total_shipments_updated}")




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