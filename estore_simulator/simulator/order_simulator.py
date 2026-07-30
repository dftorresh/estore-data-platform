import random
from database import Database
from datetime import datetime
from config_simulation import SIMULATION
from simulator.payment_simulator import process_payment
from simulator.shipment_simulator import create_shipment, reduce_inventory


def get_random_customer(db: Database):
    customers = db.fetch_all(
        """
        SELECT customer_id
        FROM Customers
        WHERE status = 'ACTIVE'
        """
    )

    return random.choice(customers)


def get_random_products(db: Database):
    total_products = random.randint(1, 5)
    products = db.fetch_all(
        """
        SELECT
            product_id,
            unit_price
        FROM Products
        WHERE active = 1
        """
    )

    return random.sample(products, total_products)


def create_order(db: Database, customer_id):
    db.execute(
        """
        INSERT INTO Orders
        (
            customer_id,
            order_date,
            order_status,
            total_amount
        )
        OUTPUT INSERTED.order_id
        VALUES
        (
            %s,
            %s,
            'PENDING',
            0
        )
        """,
        (
            customer_id,
            datetime.utcnow()
        )
    )

    return db.cursor.fetchone()["order_id"]


def create_order_items(db: Database, order_id, products):
    total = 0
    rows = []

    for product in products:
        quantity = random.randint(1, 3)
        line_total = quantity * float(product["unit_price"])
        total += line_total

        rows.append(
            (
                order_id,
                product["product_id"],
                quantity,
                product["unit_price"],
                line_total
            )
        )

    db.executemany(
        """
        INSERT INTO OrderItems
        (
            order_id,
            product_id,
            quantity,
            unit_price,
            line_total
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
        """,
        rows
    )

    return total


def finalize_order(db: Database, order_id, total):

    db.execute(
        """
        UPDATE Orders
        SET
            total_amount = %s
        WHERE order_id = %s
        """,
        (
            total,
            order_id
        )
    )


def place_order(db):
    customer = get_random_customer(db)
    products = get_random_products(db)

    order_id = create_order(
        db,
        customer["customer_id"]
    )

    total = create_order_items(
        db,
        order_id,
        products
    )

    finalize_order(
        db,
        order_id,
        total
    )

    payment_completed = process_payment(
        db,
        order_id,
        total
    )

    if not payment_completed:

        update_order_status(
            db,
            order_id,
            "PAYMENT_FAILED"
        )

        return

    update_order_status(
        db,
        order_id,
        "PAID"
    )

    shipped = create_shipment(
        db,
        order_id
    )

    if shipped:

        reduce_inventory(
            db,
            order_id
        )

        update_order_status(
            db,
            order_id,
            "SHIPPED"
        )

    else:

        update_order_status(
            db,
            order_id,
            "READY_TO_SHIP"
        )


def place_daily_orders(db: Database):
    total_orders = random.randint(
        *SIMULATION["new_orders_per_day"]
    )

    print(f"Creating {total_orders} orders...")

    for _ in range(total_orders):
        place_order(db)

    print("Orders created.")


def update_order_status(
    db,
    order_id,
    status
):

    db.execute(
        """
        UPDATE Orders
        SET
            order_status = %s
        WHERE order_id = %s
        """,
        (
            status,
            order_id
        )
    )