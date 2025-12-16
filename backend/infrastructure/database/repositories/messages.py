from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from settings import settings

from application.ports import MessagesRepositoryPort


class MessagesRepository(MessagesRepositoryPort):
    """
    MongoDB implementation of the MessagesRepositoryPort.

    This repository handles persistence of message documents using
    an AsyncIOMotorCollection. It belongs to the infrastructure layer
    and contains only storage-specific logic.
    """

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        """
        Initialize the repository with a MongoDB collection.

        Args:
            collection (AsyncIOMotorCollection): The MongoDB collection for messages.
        """
        self.collection = collection

    async def message_exists(self, filters: dict) -> bool:
        """
        Check whether a message matching the given filters exists.

        Args:
            filters (dict): Filter parameters used to locate the message.

        Returns:
            bool: True if a matching message exists, otherwise False.
        """
        if await self.collection.find_one(filters, projection={'_id': 1}) is not None:
            return True
        return False

    async def create_message(self, message: dict) -> str:
        """
        Insert a new message into the collection.

        Args:
            message (dict): The message document to be persisted.

        Returns:
            str: The identifier of the newly created message.
        """
        result = await self.collection.insert_one(document=message)
        return str(result.inserted_id)

    async def update_id(self, _id: str) -> dict | None:
        """
        Set the string 'id' field on a message document.

        Args:
            _id (str): The ObjectId (as string) that will be written into the 'id' field.
        """
        return await self.collection.find_one_and_update(
            {'_id': ObjectId(_id)},
            {'$set': {'id': _id}},
            return_document=ReturnDocument.AFTER,
        )

    async def get_chat_messages(self, filters: dict) -> list:
        """
        Retrieve a limited number of chat messages using given filters,
        sorted by newest first.

        Args:
            filters (dict): Query parameters used to filter messages.

        Returns:
            list: A list of message documents.
        """
        cursor = self.collection.find(filters).sort({'_id': -1}).limit(settings.messages_limit)
        return await cursor.to_list(length=None)
    
    async def previous_messages_exist(self, _id: str) -> bool:
        """
        Check if older messages exist before the given message ID.

        Args:
            _id (str): The identifier used as the pagination reference.

        Returns:
            bool: True if older messages exist, otherwise False.
        """
        if await self.collection.find_one({'_id': {'$lt': ObjectId(_id)}}, projection={'_id': 1}) is not None:
            return True
        return False
