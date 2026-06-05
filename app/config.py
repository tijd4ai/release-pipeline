from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str = "us-east-1"
    dynamodb_table: str = "items"
    dynamodb_endpoint_url: str | None = None  # Set for local DynamoDB

    model_config = {"env_prefix": "APP_"}


settings = Settings()
