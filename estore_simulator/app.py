import argparse
from database import Database
from simulator.initializer import initialize
from simulator.customer_simulator import register_customers
from simulator.order_simulator import place_daily_orders
from simulator.customer_updates import update_customers
from simulator.shipment_simulator import update_shipments


def test_connection():
    with Database() as db:
        version = db.fetch_one("SELECT @@VERSION as V")
        print("\nConnected successfully!\n")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize ERP master data."
    )

    parser.add_argument(
        "--simulate-day",
        action="store_true",
        help="Run one day of business activity."
    )

    args = parser.parse_args()
    test_connection()

    if args.init:
        initialize()

    if args.simulate_day:
        with Database() as db:
            register_customers(db)
            place_daily_orders(db)
            update_customers(db)
            update_shipments(db)

if __name__ == "__main__":
    main()