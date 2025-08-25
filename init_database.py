from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text

engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/reddit_pipeline")
metadata = MetaData()

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text),
    Column("score", Integer),
    Column("classification", String(50)),
)

metadata.create_all(engine)