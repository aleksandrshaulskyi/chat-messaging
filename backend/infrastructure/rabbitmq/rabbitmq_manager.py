from json import dumps

from aio_pika import connect_robust, Exchange, ExchangeType, Message, Queue

from settings import settings

from application.ports import RabbitMQManagerPort


class RabbitMQManager(RabbitMQManagerPort):
    """
    The RabbitMQ manager that orchestrats workflow with the RabbitMQ.

    Responsible for the consumption of the messages that has been published by
    the transport layer and publishing the processed messages back so that they
    can be dispatched to users.
    """

    def __init__(self) -> None:
        """
        Initialize the manager.
        """
        self.connection = None
        self.consumption_channel = None
        self.delivery_exchange: Exchange = None
        self.database_exchange: Exchange = None
        self.queue: Queue = None

    async def start(self) -> None:
        """
        Starting process.

        Create connection and channels, make sure that exchanges exist, declare the queue.
        """
        self.connection = await connect_robust(settings.rabbitmq_url)

        self.publishing_channel = await self.connection.channel(publisher_confirms=True)
        self.consumption_channel = await self.connection.channel()

        await self.consumption_channel.set_qos(prefetch_count=settings.channel_prefetch_messages_count)

        self.delivery_exchange = await self.publishing_channel.declare_exchange(
            name=settings.delivery_exchange_name,
            type=ExchangeType.DIRECT,
            durable=True,
            passive=True,
        )

        self.database_exchange = await self.consumption_channel.declare_exchange(
            name=settings.database_exchange_name,
            type=ExchangeType.DIRECT,
            durable=True,
            passive=True,
        )

        self.queue = await self.consumption_channel.declare_queue(
            name=settings.database_queue_name,
            exclusive=False,
            auto_delete=False,
            passive=True,
        )

    async def get_queue(self) -> Queue:
        """
        Get the consumption queue.

        Returns:
            Queue: The consumption queue that is an instance of RabbitMQ Queue.
        """
        return self.queue
    
    async def create_message(self, body: bytes) -> Message:
        """
        Get the instance of RabbitMQ Message to publish it to the broker.

        Args:
            body (bytes): The body of a message.

        Returns:
            Message: an instance of RabbitMQ Message.
        """
        return Message(body=body, content_type='application/json', content_encoding='utf-8')

    async def send_message(self, message_data: dict) -> None:
        """
        Send a processed message to the delivery microservice.

        Args:
            message_data: A messages in the form of a dictionary.
        """
        body = dumps(message_data).encode('utf-8')
        rabbitmq_message = await self.create_message(body=body)
        await self.delivery_exchange.publish(message=rabbitmq_message, routing_key='')
