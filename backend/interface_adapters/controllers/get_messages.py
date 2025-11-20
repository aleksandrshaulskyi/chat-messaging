from dataclasses import asdict

from application.ports import ChatRepositoryPort, MessagesRepositoryPort
from application.use_cases import GetMessagesUseCase
from interface_adapters.outgoing_dtos import OutgoingMessageDTO


class GetMessagesController:
    """
    The controller that is responsible for getting messages that
    belong to the requested chat.
    """

    def __init__(
        self,
        chat_id: str,
        user_id: int,
        cursor: str | None,
        chats_repo: ChatRepositoryPort,
        messages_repo: MessagesRepositoryPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            chat_id (str): An id of a chat.
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

    def transform_messages(self, messages: list) -> list:
        """
        Tranform messages from internal format to the outgoing format.
        """
        if not messages:
            return messages
        return [asdict(OutgoingMessageDTO.from_dict(raw_message)) for raw_message in messages]

    async def get_messages(self) -> dict:
        """
        Call the respectful use case and prepare the outgoing data.
        """
        use_case = GetMessagesUseCase(
            chat_id=self.chat_id,
            user_id=self.user_id,
            cursor=self.cursor,
            chats_repo=self.chats_repo,
            messages_repo=self.messages_repo,
        )

        messages_data = await use_case.execute()
        messages_data.messages = self.transform_messages(messages=messages_data.messages)

        return messages_data
