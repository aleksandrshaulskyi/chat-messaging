from fastapi import FastAPI

from application.exceptions import ApplicationLayerException
from infrastructure.exception_handlers import application_exception_handler


def setup_exception_handlers(application: FastAPI) -> None:
    """
    Adds all the exception handlers.
    """
    application.add_exception_handler(ApplicationLayerException, application_exception_handler)
