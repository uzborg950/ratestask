import os

import psycopg2
import pytest
from pytest_postgresql.janitor import DatabaseJanitor


@pytest.fixture
def database(postgresql_proc):
    # variable definition

    with DatabaseJanitor(
            user=postgresql_proc.user,
            host=postgresql_proc.host,
            port=postgresql_proc.port,
            dbname="my_test_database",
            version=postgresql_proc.version,
            password="secret_password",
    ):
        conn = psycopg2.connect(
            dbname="my_test_database",
            user=postgresql_proc.user,
            password="secret_password",
            host=postgresql_proc.host,
            port=postgresql_proc.port,
        )
        with conn.cursor() as cursor:
            with open(f"{os.getcwd()}/database/setup.sql") as f:
                setup_sql = f.read()
                cursor.execute(setup_sql)
                conn.commit()
        yield conn
