from abc import ABC, abstractmethod


class RabbitMQManagerPort(ABC):
    """
    The port that defines methods for the persistent operations with RabbitMQ.

    This port is used as an abstraction on the application layer.
    """

    @abstractmethod
    async def send_message(self, message_data: dict, routing_key: str) -> None:
        """
        A method that allows to send a message to RabbitMQ exchange.
        """
        ...
