from logging import getLogger

from settings import settings

from application.exceptions import ChatCreationDeniedException
from application.ports import ChatRepositoryPort, GetUsersInfoPort
from domain.entities import Chat


class CreateChatUseCase:
    """
    The use case to create a chat.
    """

    def __init__(
        self,
        user_id: int,
        create_chat_data: dict,
        database_repo: ChatRepositoryPort,
        users_info_port: GetUsersInfoPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_id (int): The id of the user that has requested to create a chat.
            create_chat_data (dict): The data that is required to create a chat.
            database_repo (ChatRepositoryPort): The port for chats collection database repository.
            users_info_port (GetUsersInfoPort): The port for the service that gets information about users.
        """
        self.user_id = user_id
        self.create_chat_data = create_chat_data
        self.database_repo = database_repo
        self.users_info_port = users_info_port
        self.logger = getLogger(settings.chats_logger_name)

    def enforce_permission_policy(self) -> None:
        """
        Enforce the authorization.

        If a user_id is not in the list of related users
        deny the chat creation.
        """
        related_user_ids = self.create_chat_data.get('user_ids')

        if self.user_id not in related_user_ids:
            self.logger.error(
                'User attempted to create a chat that he is not related to.',
                extra={'user_id': self.user_id, 'event_type': 'Unrelated user creates chat.'}
            )
            raise ChatCreationDeniedException(
                title='Chat creation is denied.',
                details={'Authorization error.': 'You are not permitted to create such chat.'}
            )
        
    def prepare_query(self, chat: Chat) -> dict:
        """
        Prepare the query to get or create an instance of the Chat in MongoDB.

        Args:
            chat: An instance of Chat.
        Returns:
            dict: A prepared query to forward to the chats repository.
        """
        related_users = sorted(chat.related_users, key=lambda related_user: related_user.get('id'))

        return {
            'filter': {'related_users': related_users},
            'update': {'$setOnInsert': chat.representation},
            'upsert': True,
            'return_document': 2,
        }
        
    async def get_users_information(self) -> list:
        """
        Call the respectful service to get the information about users
        that are related to a chat.
        """
        return await self.users_info_port.execute(user_ids=self.create_chat_data.get('user_ids'))

    async def execute(self) -> dict:
        """
        Chat creation executor.

        Enforce the authorization policy, get rich user information from
        the authentication service, if chat already exists return it and if
        it does not - create the new one.

        Returns:
            dict: An instance of a chat from the database in a format of a dictionary.
        """
        self.enforce_permission_policy()

        related_users = await self.get_users_information()

        chat_entity = Chat.create(related_users=related_users)

        query = self.prepare_query(chat=chat_entity)

        chat = await self.database_repo.get_or_create_chat(query=query)

        if chat.get('id') is None:
            _id = str(chat.get('_id'))
            await self.database_repo.update_id(_id=_id)
            chat.update({'id': _id})

        return chat
