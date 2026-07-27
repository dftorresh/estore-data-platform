import argparse

from database import get_connection
from simulator.initializer import initialize

def test_connection():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION AS v")
        version = cursor.fetchone()
        print("\nConnected successfully!\n")
        print(version)


# def initialize():
#     print("Initializing eStore ERP...")
#     print("Nothing to initialize yet.")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize ERP master data."
    )

    args = parser.parse_args()
    test_connection()

    if args.init:
        initialize()


if __name__ == "__main__":
    main()