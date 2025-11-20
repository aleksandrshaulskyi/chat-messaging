from fastapi import FastAPI

from infrastructure.handlers import chats_router, messages_router


def setup_routers(application: FastAPI) -> None:
    """
    Setup the FastAPI routers.
    """
    application.include_router(chats_router)
    application.include_router(messages_router)
