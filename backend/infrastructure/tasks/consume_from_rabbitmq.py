from asyncio import QueueFull

from dependency_injector.wiring import inject, Provide

from settings import settings

from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.incoming_dtos import IncomingMessageDTO
from infrastructure.rabbitmq import RabbitMQDecoder, RabbitMQManager
from infrastructure.transport import QueueManager


@inject
async def consume_from_rabbitmq(
    queue_manager: QueueManager = Provide[DependenciesContainer.queue_manager],
    rabbitmq_manager: RabbitMQManager = Provide[DependenciesContainer.rabbitmq_manager],
) -> None:
    """
    The RabbitMQ consumer task that decodes, validates and forwards messages to an internal messaging queue.
    """
    external_queue = await rabbitmq_manager.get_queue()
    messages_queue = await queue_manager.get_queue(collection_name=settings.messages_collection_name)

    async with external_queue.iterator() as queue_iterator:
        async for message in queue_iterator:
            async with message.process(requeue=False):
                decoded_message = await RabbitMQDecoder(message=message.body).execute()
                validated_message = IncomingMessageDTO(**decoded_message).model_dump()
                try:
                    await messages_queue.put(validated_message)
                except QueueFull:
                    message.nack(requeue=True)
