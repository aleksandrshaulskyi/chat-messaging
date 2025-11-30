from fastapi import FastAPI

from infrastructure.handlers import setup_routers
from infrastructure.exception_handlers import setup_exception_handlers
from infrastructure.logging import setup_logging
from infrastructure.middleware import setup_middleware
from infrastructure.monitoring import setup_metrics
from lifespan import lifespan


def compose_application() -> FastAPI:
    """
    Compose the application.

    - Setup exception handlers.
    - Setup routers.
    - Setup middleware.
    - Setup metrics.
    - Setup logging.

    Returns:
        FastAPI: An instance of FastAPI application.
    """
    application = FastAPI(lifespan=lifespan, root_path='/messaging')

    setup_exception_handlers(application=application)
    setup_metrics(application=application)
    setup_middleware(application=application)
    setup_routers(application=application)

    setup_logging()

    return application
