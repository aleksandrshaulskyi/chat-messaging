from dataclasses import dataclass
from interface_adapters.shared_utils import add_from_dict


@dataclass
@add_from_dict
class ChatOUTDTO:
    """
    The DTO that is used to represent an instance of Chat in responses.
    """
    id: str
    related_users: list
