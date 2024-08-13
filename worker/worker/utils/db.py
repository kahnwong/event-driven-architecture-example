import os

from dotenv import load_dotenv
from sqlmodel import create_engine

from worker.utils.log import init_logger

load_dotenv()
logger = init_logger(__name__)

POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


def get_connection_string():
    return f"postgresql+psycopg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"


def create_postgres_engine():
    logger.info(f"database: {POSTGRES_HOSTNAME}")

    return create_engine(
        get_connection_string(),
        # echo=True,
    )
