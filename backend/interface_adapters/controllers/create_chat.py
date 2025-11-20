from application.ports import ChatRepositoryPort, GetUsersInfoPort
from application.use_cases import CreateChatUseCase
from interface_adapters.outgoing_dtos import ChatOUTDTO


class CreateChatController:
    """
    This controller is responsible for the creating chats.

    It calls the respectful use case and forwards the data
    from the handler to the use case and adapts the data to
    the outgoing format afterwards.
    """

    def __init__(
        self,
        user_id: int,
        create_chat_data: dict,
        database_repo: ChatRepositoryPort,
        users_info_port: GetUsersInfoPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            user_id (int): An id of a user that has requested chat creation.
            create_chat_data (dict): Required data for chat creation.
            database_repo (ChatRepositoryPort): The port for the repository that operates with chats collection.
            users_info_port (GetUsersInfoPort): The port for the service that fetches information about users.
        """
        self.user_id = user_id
        self.create_chat_data = create_chat_data
        self.database_repo = database_repo
        self.users_info_port = users_info_port

    async def create_chat(self) -> ChatOUTDTO:
        """
        Create a chat. Call the respectful use case with the required data and adapt it
        to the outgoing format.

        Returns:
            ChatOUTDTO: An instance of Chat in the approptiate format.
        """
        use_case = CreateChatUseCase(
            user_id=self.user_id,
            create_chat_data=self.create_chat_data,
            database_repo=self.database_repo,
            users_info_port=self.users_info_port,
        )

        chat = await use_case.execute()

        return ChatOUTDTO.from_dict(chat)
