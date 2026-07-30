from datetime import datetime
import random

from config_simulation import SIMULATION

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal"
]

def process_payment(db, order_id, total_amount):

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
            payment_status
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
        """,
        (
            order_id,
            datetime.utcnow(),
            random.choice(PAYMENT_METHODS),
            total_amount,
            payment_status
        )
    )

    return success