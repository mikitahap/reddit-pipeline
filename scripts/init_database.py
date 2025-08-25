from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, text

def db_init():
    admin_engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/postgres", isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        db_exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'reddit_pipeline'")
        ).scalar()

        if not db_exists:
            conn.execute(text("CREATE DATABASE reddit_pipeline"))

    engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/reddit_pipeline")
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

    return engine, posts