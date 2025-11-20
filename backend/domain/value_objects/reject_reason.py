from enum import Enum


class RejectReason(str, Enum):
    """
    Represent a reason that a message was rejected for.
    """
    DUPLICATED = 'Duplicated client_message_id.'
    INVALID_CHAT_ID = 'An invalid chat id. Such chat does not exist in the database.'
    NOT_RELATED_TO_CHAT = 'The sender and/or the recipient are not related to the specified chat.'
