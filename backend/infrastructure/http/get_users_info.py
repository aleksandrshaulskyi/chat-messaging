from asyncio import TimeoutError

from aiohttp import ClientConnectionError, ClientError, ClientSession, ContentTypeError
from backoff import expo, on_exception, full_jitter

from settings import settings

from application.exceptions import UserInfoServiceUnavailableException, UserResponseInvalidException
from application.ports import GetUsersInfoPort


class GetUsersInfo(GetUsersInfoPort):
    """
    The service that is responsible for the retrieval of users information
    that is required for the chat creation from the authentication service.
    """

    def __init__(self) -> None:
        """
        Initialize the service.
        """
        self.url = f'{settings.auth_backend_base_url}/users/get-users-info'

    @on_exception(
        expo,
        (ClientError, TimeoutError),
        max_time=30,
        jitter=full_jitter,
    )
    async def execute(self, user_ids: list) -> list | None:
        """
        Execute the retrieval process.

        Request the endpoint. Retry for 30 seconds if request fails with the jitter.

        Returns:
            list: A list of dictionaries containing the info about requested users.

        Raises:
            UserInfoServiceUnavailableException: Raisen if server did not respond or responded with 4xx or 5xx code.
            UserResponseInvalidException: Raisen if server responded with an invalid json.
        """
        try:
            async with ClientSession() as session:
                async with session.post(url=self.url, json={'user_ids': user_ids}) as response:
                    try:
                        response.raise_for_status()
                    except ClientError:
                        raise UserInfoServiceUnavailableException(
                            title='Unprocessable response was returned.',
                            details={'Unprocessable response code.': 'Returned response with unprocessable code.'},
                        )
                    try:
                        return await response.json()
                    except ContentTypeError:
                        raise UserResponseInvalidException(
                            title='Invalid response received.',
                            details={'Invalid response.': 'Returned response is not a valid json.'},
                        )
        except (ClientConnectionError, TimeoutError):
            raise UserInfoServiceUnavailableException(
                title='External server is unavailable.',
                details={'Connection error.': 'Could not connect to a server that returns required data.'},
            )
