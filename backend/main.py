







from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lifespan import lifespan

from settings import settings

from infrastructure.handlers import chats_router, messages_router


application = FastAPI(lifespan=lifespan, root_path='/storage')

application.include_router(chats_router)
application.include_router(messages_router)

application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
