from sqlmodel import SQLModel

from backend.utils.db import create_postgres_engine

engine = create_postgres_engine()  # init postgres engine

# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
