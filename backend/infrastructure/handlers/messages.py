from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from settings import settings

from infrastructure.database import DatabaseManager
from infrastructure.database.repositories import ChatsRepository, MessagesRepository
from infrastructure.dependencies.authentication import retrieve_user_id
from infrastructure.dependency_injector import DependenciesContainer
from interface_adapters.controllers import GetMessagesController


messages_router = APIRouter(prefix='/messages')

@messages_router.get('/get-messages')
@inject
async def get_messages(
    chat_id: str,
    cursor: str | None = None,
    user_id: int = Depends(retrieve_user_id),
    database_manager: DatabaseManager = Depends(Provide[DependenciesContainer.database_manager]),
):
    """
    Get messages of a chat.
    """
    chats_collection = await database_manager.get_collection(collection_name=settings.chats_collection_name)
    messages_collection = await database_manager.get_collection(collection_name=settings.messages_collection_name)

    controller = GetMessagesController(
        chat_id = chat_id,
        user_id=user_id,
        cursor=cursor,
        chats_repo=ChatsRepository(collection=chats_collection),
        messages_repo=MessagesRepository(collection=messages_collection)
    )

    return await controller.get_messages()
