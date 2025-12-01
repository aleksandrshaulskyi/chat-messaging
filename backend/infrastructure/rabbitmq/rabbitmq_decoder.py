from logging import getLogger

from settings import settings

from json import JSONDecodeError, loads


class RabbitMQDecoder:
    """
    A decoder for RabbitMQ messages.
    """

    def __init__(self, message: bytes) -> None:
        """
        Initialize the decoder.

        Args:
            messages: A message from RabbitMQ in the bytes form.
        """
        self.message = message
        self.logger = getLogger(settings.chats_logger_name)

    async def execute(self) -> dict:
        """
        Decode message.

        Returns:
            dict: A message in the form of a dictionary.

        Raises:
            ...
        """
        try:
            self.message = self.message.decode('utf-8')
        except AttributeError:
            self.logger.error(
                f'Problem with message decoding: {self.message}',
                extra={'user_id': None, 'event_type': 'Message decoding error.'},
            )
        else:

            try:
                return loads(self.message)
            except JSONDecodeError:
                self.logger.error(
                    f'Problem with message json parsing: {self.message}',
                    extra={'user_id': None, 'event_type': 'Message json parsing error.'},
                )
