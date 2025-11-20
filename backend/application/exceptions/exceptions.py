from domain.exceptions import BaseException


class ApplicationLayerException(BaseException):
    """"
    This is the base exception for the application layer.
    All the exceptions raisen on this layer should be inherited
    from this exception.
    """


class MessagesRetrievalDeniedException(ApplicationLayerException):
    """
    This exception is raisen if a user is not permitted to retrieve
    the messages from the chat he requested because he is not related
    to such chat.
    """


class ChatCreationDeniedException(ApplicationLayerException):
    """
    This exception is raisen if a user that requested to create a chat
    is not in the list of users that are related to such chat.
    """


class UserInfoServiceUnavailableException(ApplicationLayerException):
    """
    This exception is raisen if the service that returns the information
    about the users related to a chat is unavailable.
    """


class UserResponseInvalidException(ApplicationLayerException):
    """
    This exception is raisen if the service that returns the information
    about the users related to a chat returned an unserializable response.
    """


class ChatUpdatingDeniedException(ApplicationLayerException):
    """
    This exception is raisen if the requesting user is not the user
    whos information is being updated.
    """
