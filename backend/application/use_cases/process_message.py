from application.ports import ChatRepositoryPort, MessagesRepositoryPort, RabbitMQManagerPort
from domain.entities import Message
from domain.value_objects import RejectReason


class ProcessMessageUseCase:
    """
    Process messages use case.

    This use case is responsible for the processing of a single message.
    It executes following procedures:
    - Attempts to create a domain entity of the Message.
    - Stores an instance of the Message to the database.
    - Increments the count of related messages for the respectful chat.
    - Sends a message back to the RabbitMQ so that it can be later dispatched
    back to a user.
    """

    def __init__(
        self,
        message: dict,
        chats_repo: ChatRepositoryPort,
        messages_repo: MessagesRepositoryPort,
        rabbitmq_manager: RabbitMQManagerPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            message (dict): A message data in the form of a dictionary.
            chats_repo (ChatRepositoryPort): The port for a repository responsible for database actions with chats.
            messages_repo (MessagesRepositoryPort): The port for a repository responsible for actions with messages.
            rabbitmq_manager (RabbitMQManagerPort): The port for RabbitMQ manager.
        """
        self.message = message
        self.chat = None
        self.chats_repo = chats_repo
        self.messages_repo = messages_repo
        self.rabbitmq_manager = rabbitmq_manager

    async def execute(self) -> None:
        """
        Execute the processing process.
        """
        self.prepare()

        if await self.validate():
            if await self.enforce_permission_policy():
                await self.create_message()
                await self.increment_messages_count()

        await self.send_message()

    def prepare(self) -> None:
        """
        Create an instance of a Message entity.
        """
        self.message = Message.create(message_data=self.message)

    async def validate(self) -> bool:
        message_accepted = await self.validate_message()
        chat_accepted = await self.validate_chat()

        return all({message_accepted, chat_accepted})

    async def validate_message(self) -> bool:
        """
        Validate the message.

        If message is considered invalid it's status will be changed to rejected
        with a valid reject reason and it will be afterwards sent to the sender.
        """
        message_filters = {'client_message_id': self.message.client_message_id}
        message_exists = await self.messages_repo.message_exists(filters=message_filters)

        if message_exists:
            self.message.reject(reject_reason=RejectReason.DUPLICATED)
            return False
        
        return True
    
    async def validate_chat(self) -> bool:
        """
        Validate the chat that is specified in the message.
        """
        chat = await self.chats_repo.get_chat(id=self.message.chat_id)

        if chat is None:
            self.message.reject(reject_reason=RejectReason.INVALID_CHAT_ID)
            return False
        
        self.chat = chat
        return True

    async def enforce_permission_policy(self) -> bool:
        """
        Enforce the authorization policy.

        A message will be accepted if only both sender and recipient related to the
        chat specified in message.
        """
        related_chat_users = {user.get('id') for user in self.chat.get('related_users')}
        related_message_users = {self.message.sender_id, self.message.recipient_id}

        if related_chat_users != related_message_users:
            self.message.reject(reject_reason=RejectReason.NOT_RELATED_TO_CHAT)
            return False
        return True

    async def create_message(self) -> None:
        """
        Store a message to the database and update it's id based on MongoDB auto generated _id.
        """
        inserted_id = await self.messages_repo.create_message(message=self.message.representation)

        processed_message_data = await self.messages_repo.update_id(_id=inserted_id)

        self.message = Message.create(message_data=processed_message_data)

    async def increment_messages_count(self) -> None:
        """
        Increment the count of messages of a chat that a message belongs to.
        """
        await self.chats_repo.increment_messages_count(id=self.message.chat_id)

    async def send_message(self) -> None:
        """
        Send a message to the RabbitMQ exchange for further dispatching.
        """
        await self.rabbitmq_manager.send_message(message_data=self.message.representation)
