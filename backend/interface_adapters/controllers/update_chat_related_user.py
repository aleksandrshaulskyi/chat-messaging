from application.ports import ChatRepositoryPort
from application.use_cases import UpdateChatUserUseCase


class UpdateChatRelatedUserController:
    """
    This controller is responsible for the update of chats
    related users upon update information about users by themselves.
    """

    def __init__(self, user_data: dict, user_id: int, database_repo: ChatRepositoryPort) -> None:
        """
        Initialize the controller.

        Args:
            user_data (dict): A dictionary containing the data that is needed to update chats.
            user_id (int): The id of requesting user.
            database_repo (ChatRepositoryPort): The port that defines operations with the chats.
        """
        self.user_data = user_data
        self.user_id = user_id
        self.database_repo = database_repo

    async def update_chat_related_user(self) -> None:
        """
        Update chtas related user.
        """
        use_case = UpdateChatUserUseCase(
            user_data=self.user_data,
            user_id=self.user_id,
            database_repo=self.database_repo,
        )

        await use_case.execute()
