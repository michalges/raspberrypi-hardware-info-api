from duckdb import DuckDBPyConnection


def create_tables(db_connection: DuckDBPyConnection):
    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS system_metrics (
            timestamp TIMESTAMPTZ PRIMARY KEY,
            cpu_usage FLOAT NULL,
            temp FLOAT NULL,
            ram_usage FLOAT NULL,
            storage_usage FLOAT NULL
        )
    """
    )
