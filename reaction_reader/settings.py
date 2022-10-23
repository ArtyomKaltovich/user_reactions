from pydantic import BaseSettings


class Settings(BaseSettings):
    dbname: str = "postgres"
    dbuser: str = "postgres"
    dbpassword: str = "users_reactions_super"
    dbhost: str = "192.168.56.101"
    dbport: int = 5432
    update_reactions_period: float = 1.0  # in seconds
    dbcommand_timeout: float = 30.0  # in seconds
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
