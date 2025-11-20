







from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from infrastructure.exceptions import AuthenticationException
from infrastructure.security import JWTManager


async def retrieve_user_id(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int | None:
    """
    Retrieve the requesting user_id from authorization header.

    Returns:
        int: The requesting user_id if credentials provided are valid.

    Raises:
        HTTPException: If the credentials are missing or invalid.
    """
    if not (access_token := credentials.credentials):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='No token was provided.'
        )
    
    try:
        return await JWTManager().retrieve_user_id(token=access_token)
    except AuthenticationException as exception:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=exception.representation,
        )
