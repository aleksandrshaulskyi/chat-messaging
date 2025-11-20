from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #BASE
    messages_limit: int = 10
    auth_backend_base_url: str = 'http://auth_backend:8000'
    default_datetime_format: str = '%Y-%m-%dT%H:%M:%S.%fZ'
    min_username_length: int = 4

    #SECURITY
    key: str = Field(validation_alias='KEY')
    algorithm: str = Field(validation_alias='ALGORITHM')

    #DATABASE
    mongo_url: str = Field(validation_alias='MONGO_URL')
    mongo_database_name: str = Field(validation_alias='MONGO_DATABASE_NAME')
    messages_collection_name: str = 'messages'
    chats_collection_name: str = 'chats'

    #RABBITMQ
    rabbitmq_url: str = Field(validation_alias='RABBITMQ_URL')
    websockets_exchange_name: str = Field(validation_alias='WEBSOCKETS_EXCHANGE_NAME')
    database_exchange_name: str = Field(validation_alias='DATABASE_EXCHANGE_NAME')
    database_queue_name: str = Field(validation_alias='DATABASE_QUEUE_NAME')
    
    #CORS
    cors_origins: list = ['http://localhost:3000']

    model_config = {
        'env_file': '.env',
        'extra': 'allow',
    }

settings = Settings()
