from sqlmodel import create_engine, Session

engine = create_engine("duckdb:///system_metrics.duckdb")


def get_session():
    with Session(engine) as session:
        yield session
