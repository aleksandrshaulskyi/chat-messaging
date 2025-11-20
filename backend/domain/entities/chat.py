from dataclasses import asdict, dataclass


@dataclass
class Chat:
    """
    The domain entity of Chat.

    This entity holds the relation between users as well as
    all the important information about such relation.

    Attributes:
        id: The id of a Chat.
        related_user_ids: A list of ids of the users that are communicating through this chat.
        related_users: A list of user ids which are going to be communicating through this chat.
        messages_count: The amount of messages that are related to this chat.
    """
    id: int | None
    related_users: list
    messages_count: int

    @property
    def representation(self) -> dict:
        """
        Convert the chat entity into a serializable dictionary.

        Used for JSON serialization.

        Returns:
            dict: The serializible representation of the Chat entity.
        """
        return asdict(self)

    @classmethod
    def create(cls, related_users: list) -> 'Chat':
        """
        Factory method for constructing a new Chat entity.

        Args:
            chat_data (dict): Clean validated data from the application layer.

        Returns:
            Chat: A new Chat object.
        """
        related_users = sorted(related_users, key=lambda related_user: related_user.get('id'))

        return Chat(
            id=None,
            related_users=related_users,
            messages_count=0,
        )
