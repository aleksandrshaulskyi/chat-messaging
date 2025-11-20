from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorCollection

from application.ports import ChatRepositoryPort


class ChatsRepository(ChatRepositoryPort):
    """
    MongoDB implementation of the ChatRepositoryPort.

    This repository performs all persistence operations for chats using
    an AsyncIOMotorCollection. It is part of the infrastructure layer and
    contains only database-specific logic.
    """

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        """
        Initialize the repository with a MongoDB collection.

        Args:
            collection (AsyncIOMotorCollection): The MongoDB collection for chats.
        """
        self.collection = collection

    async def get_or_create_chat(self, query: dict) -> dict:
        """
        Retrieve a chat matching the query or create one using upsert semantics.

        Args:
            query (dict): The parameters passed to find_one_and_update (filter, update, upsert).

        Returns:
            dict: The chat document that was found or created.
        """
        return await self.collection.find_one_and_update(**query)

    async def update_id(self, _id: str) -> None:
        """
        Set the string 'id' field on a chat document.

        Args:
            _id (str): The ObjectId (as string) that should be written into the 'id' field.
        """
        await self.collection.update_one({'_id': ObjectId(_id)}, {'$set': {'id': _id}})

    async def get_chat(self, id: str) -> dict | None:
        """
        Retrieve a chat by its string identifier.

        Args:
            id (str): The chat identifier stored in the 'id' field.

        Returns:
            dict | None: The chat document if found, otherwise None.
        """
        return await self.collection.find_one({'id': id})

    async def get_chats(self, filters: dict) -> list:
        """
        Retrieve all chats matching the given filter criteria.

        Args:
            filters (dict): The filter parameters for the MongoDB query.

        Returns:
            list: A list of chat documents.
        """
        cursor = self.collection.find(filters)
        return await cursor.to_list(length=None)
    
    async def increment_messages_count(self, id: str) -> None:
        """
        Atomically increase the messages_count field of a chat.

        Args:
            id (str): The identifier of the chat whose message counter should be incremented.
        """
        await self.collection.update_one({'id': id}, {'$inc': {'messages_count': 1}})

    async def update_related_user(self, user_id: int, user_data: dict) -> None:
        """
        Updates all chats that the user with the provided user_id is related to.
        """
        await self.collection.update_many({'related_users.id': user_id}, {'$set': {'related_users.$': user_data}})
