import argparse

from database import Database
from simulator.initializer import initialize


def test_connection():

    with Database() as db:

        version = db.fetch_one("SELECT @@VERSION as V")

        print("\nConnected successfully!\n")

        print(version)


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