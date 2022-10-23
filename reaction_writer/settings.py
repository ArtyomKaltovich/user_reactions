from pydantic import BaseSettings


class Settings(BaseSettings):
    dbname: str = "postgres"
    dbuser: str = "postgres"
    dbpassword: str = "users_reactions_super"
    dbhost: str = "0.0.0.0"
    dbport: int = 5432
    dbpool_min_size: int = 1
    dbpool_max_size: int = 10
    dbpool_command_timeout: int = 60
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
