from dataclasses import dataclass


@dataclass
class OutgoingMessagesDTO:
    """
    A data transfer object representing a batch of messages returned to the client.

    This DTO is used by the application layer to send formatted message data
    to the transport layer (e.g., WebSocket or HTTP handler). It contains the
    list of messages, the cursor for pagination, and a flag indicating whether
    older messages exist.

    Attributes:
        messages (list): 
            A list of message representations (usually dictionaries) that are ready
            to be sent to the client.

        cursor (str): 
            The identifier of the latest message in the current batch. Used as
            a pagination cursor to fetch earlier messages.

        previous_messages_exist (bool): 
            A flag that indicates whether there are messages older than the ones
            included in this batch.
    """
    messages: list
    cursor: str
    previous_messages_exist: bool
