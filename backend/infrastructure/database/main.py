from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from settings import settings


class DatabaseManager:

    def __init__(self) -> None:
        self.client = None
        self.database = None
        self.collections = {
            'messages': None,
            'chats': None,
        }

    async def start(self) -> None:
        self.client = AsyncIOMotorClient(host=settings.mongo_url)
        self.database = self.client[settings.mongo_database_name]

        database_list_of_collection_names = await self.database.list_collection_names()

        for collection_name in self.collections:
            if collection_name not in database_list_of_collection_names:
                self.collections[collection_name] = await self.database.create_collection(name=collection_name)
            else:
                self.collections[collection_name] = self.database[collection_name]

    async def get_collection(self, collection_name) -> AsyncIOMotorCollection:
        return self.collections.get(collection_name)
