from application.ports import ChatRepositoryPort


class GetChatsUseCase:
    """
    Get a user's chats.

    This use case is responsible for retrieving the chats
    that the requesting user is related to.
    """

    def __init__(self, user_id: int, database_repo: ChatRepositoryPort) -> None:
        """
        Initialize the use case.

        Args:
            user_id (int): The id of a user.
            database_repo (ChatRepositoryPort): The port for chats collection database repository.
        """
        self.user_id = user_id
        self.database_repo = database_repo

    async def execute(self) -> list:
        """
        Execute the retrieval process.
        """
        filters = await self.create_filters()

        return await self.database_repo.get_chats(filters=filters)
    
    async def create_filters(self) -> dict:
        """
        Create filters for the database query.
        """
        filters = {'related_users.id': self.user_id, 'messages_count': {'$gt': 0}}

        return filters
