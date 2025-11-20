from abc import ABC, abstractmethod


class GetUsersInfoPort(ABC):
    """
    This is the port for an http service that requests the data
    about provided users from the authentication service.
    """
    
    @abstractmethod
    async def execute(self, user_ids: list) -> list:
        """
        Get the information about users.

        Args:
            user_ids (list): A list of user ids.

        Returns:
            list: A list of dictionaries containg the information about users or an empty list if such dont exist.
        """
        ...