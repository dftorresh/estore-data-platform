from datetime import datetime
import random

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal"
]

def process_payment(db, order_id, total_amount):

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
            %s,%s,%s,%s,'COMPLETED'
        )
        """,
        (
            order_id,
            datetime.utcnow(),
            random.choice(PAYMENT_METHODS),
            total_amount
        )
    )