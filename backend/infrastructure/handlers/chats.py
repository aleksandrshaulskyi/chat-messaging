from http import HTTPStatus

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from settings import settings

from infrastructure.database import DatabaseManager
from infrastructure.database.repositories import ChatsRepository
from infrastructure.dependencies import retrieve_user_id
from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.http import GetUsersInfo
from infrastructure.incoming_dtos import CreateChatDataDTO, UpdateChatRelatedUser
from interface_adapters.controllers import CreateChatController, GetChatsController, UpdateChatRelatedUserController
from interface_adapters.outgoing_dtos import ChatOUTDTO


chats_router = APIRouter(prefix='/chats')

@chats_router.post('/')
@inject
async def create_chat(
    create_chat_data: CreateChatDataDTO,
    user_id: int = Depends(retrieve_user_id),
    database_manager: DatabaseManager = Depends(Provide[DependenciesContainer.database_manager]),
) -> ChatOUTDTO:
    """
    Create a chat.
    """
    collection = await database_manager.get_collection(collection_name=settings.chats_collection_name)

    controller = CreateChatController(
        user_id=user_id,
        create_chat_data=create_chat_data.model_dump(),
        database_repo=ChatsRepository(collection=collection),
        users_info_port=GetUsersInfo(),
    )

    return await controller.create_chat()

@chats_router.get('/get-chats')
@inject
async def get_chats(
    user_id: int = Depends(retrieve_user_id),
    database_manager: DatabaseManager = Depends(Provide[DependenciesContainer.database_manager])
) -> list:
    """
    Get user's chats.
    """
    collection = await database_manager.get_collection(collection_name=settings.chats_collection_name)
    controller = GetChatsController(
        user_id=user_id,
        database_repo=ChatsRepository(collection=collection),
    )

    return await controller.get_chats()

@chats_router.post('/update-chat-related-user')
@inject
async def update_chat_related_user(
    user: UpdateChatRelatedUser,
    user_id: int = Depends(retrieve_user_id),
    database_manager: DatabaseManager = Depends(Provide(DependenciesContainer.database_manager))
) -> Response:
    """
    Update chats that the requesting user is related to.
    """
    collection = await database_manager.get_collection(collection_name=settings.chats_collection_name)
    controller = UpdateChatRelatedUserController(
        user_data=user.model_dump(),
        user_id=user_id,
        database_repo=ChatsRepository(collection=collection),
    )

    await controller.update_chat_related_user()

    return Response(status_code=HTTPStatus.NO_CONTENT)
