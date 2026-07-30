import random
from faker import Faker
from config_simulation import SIMULATION

fake = Faker()


def update_customers(db):

    total_customers_updated = 0
    total_addresses_updated = 0

    total = random.randint(
        *SIMULATION["customer_updates_per_day"]
    )

    customers = db.fetch_all(
        """
        SELECT customer_id
        FROM Customers
        ORDER BY NEWID()
        """
    )

    if not customers:
        return

    customers = customers[:total]

    for customer in customers:

        if random.choice([True, False]):

            db.execute(
                """
                UPDATE Customers
                SET
                    phone = %s,
                    updated_at = GETUTCDATE()
                WHERE customer_id = %s
                """,
                (
                    fake.phone_number(),
                    customer["customer_id"]
                )
            )

            total_customers_updated += 1

        else:

            db.execute(
                """
                UPDATE Addresses
                SET
                    address_line1 = %s,
                    city = %s,
                    state = %s,
                    updated_at = GETUTCDATE()
                WHERE customer_id = %s
                  AND address_type = 'Shipping'
                """,
                (
                    fake.street_address(),
                    fake.city(),
                    fake.state(),
                    customer["customer_id"]
                )
            )

            total_addresses_updated += 1

    print(f"Customers updated: {total_customers_updated}")
    print(f"Addresses updated: {total_addresses_updated}")