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
        except (AttributeError, LookupError, TypeError, UnicodeDecodeError):
            pass
        else:

            try:
                return loads(self.message)
            except JSONDecodeError:
                pass
