from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from infrastructure.database import DatabaseManager
from infrastructure.transport import QueueManager
from infrastructure.rabbitmq import RabbitMQManager


class DependenciesContainer(DeclarativeContainer):
    database_manager = Singleton(DatabaseManager)
    queue_manager = Singleton(QueueManager)
    rabbitmq_manager = Singleton(RabbitMQManager)
