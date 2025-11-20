from pydantic import BaseModel


class IncomingMessageDTO(BaseModel):
    """
    The DTO used to validate the incoming data that is received from
    the RabbitMQ to create a Message.
    """
    client_message_id: str
    chat_id: str
    sender_id: int
    recipient_id: int
    sent_at: str
    body: str
