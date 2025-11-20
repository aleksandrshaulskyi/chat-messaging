







from asyncio import create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.tasks import consume_from_rabbitmq, process_messages


@asynccontextmanager
async def lifespan(application: FastAPI):
    dependencies_container = DependenciesContainer()
    dependencies_container.wire(
        modules=[
            'infrastructure.handlers.chats',
            'infrastructure.handlers.messages',
            'infrastructure.tasks.consume_from_rabbitmq',
            'infrastructure.tasks.process_messages',
        ]
    )

    database_manager = dependencies_container.database_manager()
    rabbitmq_manager = dependencies_container.rabbitmq_manager()

    await database_manager.start()
    await rabbitmq_manager.start()

    consumption_task = create_task(consume_from_rabbitmq())
    processing_task = create_task(process_messages())

    try:
        yield
    finally:
        await consumption_task.cancel()
        await processing_task.cancel()
