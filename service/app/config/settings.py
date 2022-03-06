from pydantic import BaseSettings, Field


class Config(BaseSettings):
    service_name: str = Field(..., env="SERVICE")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=80, env="APP_PORT")
    database_uri: str = Field(..., env="DATABASE_URI")
    rabbitmq_uri: str = Field(
        default="amqp://test:test@rabbitmq:5672", env="RABBITMQ_URI"
    )
    rabbitmq_max_retries: int = Field(default=100, env="RABBITMQ_MAX_RETRIES")
    broker_routing_key: str = Field(default="tasks_queue", env="BROKER_ROUTING_KEY")


settings = Config()
