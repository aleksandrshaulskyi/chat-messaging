from pydantic import BaseModel, Field

from settings import settings


class CreateChatDataDTO(BaseModel):
    """
    This DTO is used to validate the format of the data
    that is used for the creation of chats.
    """
    user_ids: list


class UpdateChatRelatedUser(BaseModel):
    """
    This DTO is used to validate the format of the data
    that is used to update chats that the requesting user
    is related to.
    """
    id: int
    username: str = Field(..., min_length=settings.min_username_length)
    email: str
    avatar_url: str
