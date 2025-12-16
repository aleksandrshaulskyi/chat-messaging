from abc import ABC, abstractmethod


class MessagesRepositoryPort(ABC):
    """
    The port that defines persistence operations for Message entities.

    This interface belongs to the application layer and abstracts away
    message-storage logic (MongoDB, SQL, etc.). The infrastructure layer
    must provide an implementation that satisfies this contract.
    """

    @abstractmethod
    async def message_exists(self, filters: dict) -> bool:
        """
        Check whether a message exists matching the given criteria.

        Args:
            filters (dict): Filter parameters (e.g., sender_id, client_message_id).

        Returns:
            bool: True if a matching message exists, otherwise False.
        """
        ...

    @abstractmethod
    async def create_message(self, message: dict) -> str:
        """
        Persist a new message and return its identifier.

        Args:
            message (dict): A dictionary containing message data.

        Returns:
            str: The string identifier of the newly created message.
        """
        ...

    @abstractmethod
    async def update_id(self, _id: str) -> dict | None:
        """
        Set the string 'id' field of an existing message.

        Args:
            _id (str): The database-generated identifier to assign to the message.
        """
        ...

    @abstractmethod
    async def get_chat_messages(self, filters: dict) -> list:
        """
        Retrieve all messages for a chat using given filters.

        Args:
            filters (dict): Filter parameters for message retrieval.

        Returns:
            list: A list of message documents.
        """
        ...

    @abstractmethod
    async def previous_messages_exist(self, _id: str) -> bool:
        """
        Check whether a message with _id older than provided exists.

        Args:
            _id (str): An _id of a message.
        
        Returns:
            bool: True if at least a single message exists and False otherwise.
        """
        ...
