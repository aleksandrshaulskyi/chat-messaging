from dependency_injector.wiring import inject, Provide

from settings import settings

from infrastructure.database import DatabaseManager
from infrastructure.database.repositories import ChatsRepository, MessagesRepository
from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.rabbitmq import RabbitMQManager
from infrastructure.transport import QueueManager
from interface_adapters.controllers import ProcessMessageController


@inject
async def process_messages(
    database_manager: DatabaseManager = Provide[DependenciesContainer.database_manager],
    queue_manager: QueueManager = Provide[DependenciesContainer.queue_manager],
    rabbitmq_manager: RabbitMQManager = Provide[DependenciesContainer.rabbitmq_manager],
) -> None:
    """
    The task that consumes messages from the internal messaging queue and calls
    the designated controller for further message processing.
    """
    chats_collection = await database_manager.get_collection(collection_name=settings.chats_collection_name)
    messages_collection = await database_manager.get_collection(collection_name=settings.messages_collection_name)
    chats_repo = ChatsRepository(collection=chats_collection)
    messages_repo = MessagesRepository(collection=messages_collection)
    messages_queue = await queue_manager.get_queue(collection_name=settings.messages_collection_name)

    while True:
        message = await messages_queue.get()
        controller = ProcessMessageController(
            message=message,
            chats_repo=chats_repo,
            messages_repo=messages_repo,
            rabbitmq_manager=rabbitmq_manager,
        )

        await controller.process_message()
