







from application.exceptions import ChatUpdatingDeniedException
from application.ports import ChatRepositoryPort


class UpdateChatUserUseCase:
    """
    The use case that updates the chats which user that triggered the action is related to.
    """

    def __init__(self, user_data: dict, user_id: int, database_repo: ChatRepositoryPort) -> None:
        """
        Initialize the use case.

        Args:
            user_data (dict): A dictionary containing the data that is needed to update chats.
            user_id (int): The id of requesting user.
            database_repo (ChatRepositoryPort): The port that defines operations with the chats.
        """
        self.user_data = user_data
        self.user_id = user_id
        self.database_repo = database_repo

    def enforce_authorization_policy(self) -> None:
        """
        Validate that the requesting user is the same user whos information is being updated.

        Raises:
            ChatUpdatingDeniedException: Raisen if the requesting user is not the same user
            whos information is being updated.
        """
        if self.user_id != self.user_data.get('id'):
            raise ChatUpdatingDeniedException(
                title='Chat updating is denied.',
                details={'Chat updating is denied.': 'You are not permitted to update the chats with such info.'}
            )

    async def execute(self) -> None:
        """
        Execute the process.
        """
        self.enforce_authorization_policy()

        user_id = self.user_data.get('id')
        await self.database_repo.update_related_user(user_id=user_id, user_data=self.user_data)
