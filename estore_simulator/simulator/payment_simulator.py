from datetime import datetime
import random

from config_simulation import SIMULATION

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal"
]

def process_payment(db, order_id, total_amount):

    current_datetime =  datetime.utcnow()

    success = random.randint(
        1,
        100
    ) <= SIMULATION["payment_success_rate"]

    payment_status = (
        "COMPLETED"
        if success
        else "FAILED"
    )

    db.execute(
        """
        INSERT INTO Payments
        (
            order_id,
            payment_date,
            payment_method,
            amount,
            payment_status,
            updated_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
        """,
        (
            order_id,
            current_datetime,
            random.choice(PAYMENT_METHODS),
            total_amount,
            payment_status,
            current_datetime
        )
    )

    return success