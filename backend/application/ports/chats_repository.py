from abc import ABC, abstractmethod


class ChatRepositoryPort(ABC):
    """
    The port that defines the persistence operations for Chat entities.

    This interface is implemented on the infrastructure layer and used by
    application use cases. It abstracts away any database-related logic
    and exposes only the operations required by the domain/application layer.
    """

    @abstractmethod
    async def get_or_create_chat(self, query: dict) -> dict:
        """
        Retrieve a chat matching the given query or create a new one if it does not exist.

        Args query (dict): A dictionary containing the search filter and update parameters.

        Returns:
            dict: A dictionary representation of the chat that was found or created.
        """
        ...

    @abstractmethod
    async def update_id(self, _id: str) -> None:
        """
        Assign the string identifier 'id' to an existing chat document.

        Args _id (str): The database-generated ObjectId (as a string) that should be copied
                        into the 'id' field of the chat document.
        """
        ...

    @abstractmethod
    async def get_chat(self, id: str) -> dict | None:
        """
        Fetch a chat by its string identifier.

        Args id (str): The identifier of the chat.

        Returns (dict | None): The chat document if found, otherwise None.
        """
        ...

    @abstractmethod
    async def get_chats(self, filters: dict) -> list:
        """
        Retrieve a list of chats that match the given filter criteria.

        Args filters (dict): A dictionary of filtering options (e.g., related user IDs).

        Returns list: A list of chat documents matching the filter.
        """
        ...

    @abstractmethod
    async def increment_messages_count(self, id: str) -> None:
        """
        Atomically increment the messages_count of a chat.

        Args id (str): The identifier of the chat whose messages_count should be increased.
        """
        ...

    @abstractmethod
    async def update_related_user(self, user_id: int, user_data: dict) -> None:
        """
        Updates all chats that the user with the provided user_id is related to.
        """
        ...
