import keyring

keyring.set_password("system", "my_service_postgres_user", "postgres")
keyring.set_password("system", "my_service_postgres_password", "postgres-password")
