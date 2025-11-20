from application.ports import ChatRepositoryPort, MessagesRepositoryPort, RabbitMQManagerPort
from application.use_cases import ProcessMessageUseCase


class ProcessMessageController:
    """
    The controller that receives the data from the internal messages queue,
    transforms it to the application format and calls designated use cases.
    """

    def __init__(
        self,
        message: dict,
        chats_repo: ChatRepositoryPort,
        messages_repo: MessagesRepositoryPort,
        rabbitmq_manager: RabbitMQManagerPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            message (dict): A message data in the form of a dictionary.
            chats_repo (ChatRepositoryPort): The port for a repository responsible for database actions with chats.
            messages_repo (MessagesRepositoryPort): The port for a repository responsible for actions with messages.
            rabbitmq_manager (RabbitMQManagerPort): The port for RabbitMQ manager.
        """
        self.message = message
        self.chats_repo = chats_repo
        self.messages_repo = messages_repo
        self.rabbitmq_manager = rabbitmq_manager

    async def process_message(self) -> None:
        """
        Process a message.

        Just call the designated use case in order to process a message.
        """
        use_case = ProcessMessageUseCase(
            message=self.message,
            chats_repo=self.chats_repo,
            messages_repo=self.messages_repo,
            rabbitmq_manager=self.rabbitmq_manager,
        )

        await use_case.execute()
