from application.ports import ChatRepositoryPort
from application.use_cases import GetChatsUseCase

from interface_adapters.outgoing_dtos import ChatOUTDTO


class GetChatsController:
    """
    The controller that is responsible for retrieving a user's chats.

    Calls the respectful use case and adapts the data to the
    outgoing format.
    """

    def __init__(self, user_id: int, database_repo: ChatRepositoryPort) -> None:
        """
        Initialize the controller.

        Args:
            user_id (int): The id of requesting user.
            database_repo (ChatRepositoryPort): The port for chats collection database repository.
        """
        self.user_id = user_id
        self.database_repo = database_repo

    async def get_chats(self) -> list:
        """
        Get chats.
        """
        use_case = GetChatsUseCase(
            user_id=self.user_id,
            database_repo=self.database_repo,
        )

        chats = await use_case.execute()

        return [ChatOUTDTO.from_dict(chat) for chat in chats]
