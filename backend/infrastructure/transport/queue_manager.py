from asyncio import Queue


class QueueManager:
    """
    A simple manager that stores and provides access to internal asyncio queues.

    This component is used inside the application layer to route different
    asynchronous tasks (e.g., storing messages, delivering messages, etc.)
    through named queues.
    """

    def __init__(self) -> None:
        """
        Initialize the manager and create predefined queues.
        """
        self.queues = {
            'messages': Queue(),
        }

    async def get_queue(self, collection_name: str) -> Queue:
        """
        Retrieve a queue by its name.

        Args:
            collection_name (str): The name of the queue to retrieve.

        Returns:
            Queue: The asyncio.Queue instance associated with the name.
        """
        return self.queues.get(collection_name)

