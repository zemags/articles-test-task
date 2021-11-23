import os

from databases import Database
from sqlalchemy import create_engine, MetaData, Column, Text, String, Integer, \
    Table

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

articles = Table(
    "articles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("text", Text),
    Column("version", Integer, nullable=False)
)

database = Database(DATABASE_URL)
