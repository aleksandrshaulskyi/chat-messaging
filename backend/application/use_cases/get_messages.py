from bson import ObjectId
from logging import getLogger

from settings import settings

from application.exceptions import MessagesRetrievalDeniedException
from application.outgoing_dtos import OutgoingMessagesDTO
from application.ports import ChatRepositoryPort, MessagesRepositoryPort


class GetMessagesUseCase:
    """
    The use case that retrieves the messages of the requested chat.
    """

    def __init__(
        self,
        chat_id: str,
        user_id: int,
        cursor: str,
        chats_repo: ChatRepositoryPort, 
        messages_repo: MessagesRepositoryPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            chat_id (int): An id of a chat.
            user_id (int): An id of requesting user.
            cursor (str | None): An id of a messaget that is used as a filter.
            chats_repo (ChatRepositoryPort): The port for chats collection database repository.
            messages_repo (MessagesRepositoryPort): The port for messages collection database repository.
        """
        self.chat_id = chat_id
        self.user_id = user_id
        self.cursor = cursor
        self.chats_repo = chats_repo
        self.messages_repo = messages_repo
        self.logger = getLogger(settings.chats_logger_name)

    def make_filters(self) -> dict:
        """
        Make filters that will be used for the database query.

        Returns:
            dict: The filters in the format of a dictionary.
        """
        filters = {
            'chat_id': self.chat_id,
            '$or': [
                {'sender_id': self.user_id},
                {'recipient_id': self.user_id},
            ]
        }

        if self.cursor is not None:
            filters.update({'_id': {'$lt': ObjectId(self.cursor)}})

        return filters
        
    async def enforce_permission_policy(self) -> None:
        """
        Enforce the authorization.

        If the requesting user is not related to the requested chat - deny messages retrieval.
        """
        requested_chat = await self.chats_repo.get_chat(id=self.chat_id)
        related_users = requested_chat and requested_chat.get('related_users')

        if not any({related_user.get('id') == self.user_id for related_user in related_users}):
            self.logger.error(
                'An attempt to retrieve messages of a chat that request user is not related to.',
                extra={'user_id': self.user_id, 'event_type': 'Messages requested by unrelated user.'}
            )
            raise MessagesRetrievalDeniedException(
                title='Message retrieval is denied.',
                details={'Authorization error': 'You are not permitted to retrieve the messages of this chat.'},
            )
        
    async def make_outgoing_data(self, messages: list) -> OutgoingMessagesDTO:
        """
        Prepare the outgoing data.

        Cursor pagination is implemented for this endpoint.
        The outgoing data should contain the cursor and the flag
        that is used to check if there are more messages in the requested chat.

        Args:
            messages (list): A list of messages that belong to the requested chat.

        Returns:
            OutfoinfMessagesDTO: The dataclass that presents the data in the appropriate format.
        """
        messages_data = {
            'messages': messages,
            'cursor': '',
            'previous_messages_exist': False,
        }

        try:
            latest_message = messages[-1]
        except IndexError:
            return OutgoingMessagesDTO(**messages_data)
        else:
            cursor = str(latest_message.get('_id'))
            previous_messages_exist = await self.messages_repo.previous_messages_exist(_id=cursor)

            messages_data.update({'cursor': cursor, 'previous_messages_exist': previous_messages_exist})

            return OutgoingMessagesDTO(**messages_data)

    async def execute(self) -> OutgoingMessagesDTO:
        """
        Execute the use case.

        Enforce authorization policy, make filters, get messages and return them
        in the respectful format.

        Returns:
            OutgoingMessagesDTO: The dataclass that presents the data in the appropriate format.
        """
        await self.enforce_permission_policy()

        filters = self.make_filters()

        messages = await self.messages_repo.get_chat_messages(filters=filters)

        return await self.make_outgoing_data(messages=messages)
