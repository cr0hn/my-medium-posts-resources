import psycopg
import keyring

pg_user = keyring.set_password("system", "my_service_postgres_user")
pg_password = keyring.set_password("system", "my_service_postgres_password")

# Connect to an existing database
with psycopg.connect(f"dbname=test user={pg_user} password={pg_password}") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("""SELECT * FROM USERS""")
