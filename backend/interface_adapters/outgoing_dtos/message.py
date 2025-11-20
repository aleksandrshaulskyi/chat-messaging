from dataclasses import dataclass

from interface_adapters.shared_utils import add_from_dict


@dataclass
@add_from_dict
class OutgoingMessageDTO:
    """
    The dataclass that is used for the external Message representation.
    """
    id: int | None
    client_message_id: str
    chat_id: int | None
    sender_id: int
    recipient_id: int
    status: str
    sent_at: str
    delivered_at: str
    body: str
    is_edited: bool
    is_deleted: bool
    reject_reason: str | None = None
