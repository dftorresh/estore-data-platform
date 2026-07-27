from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "server": os.getenv("DB_SERVER"),
    "port": int(os.getenv("DB_PORT", 1433)),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
}