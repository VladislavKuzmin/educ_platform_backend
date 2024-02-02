from fastapi import APIRouter

client_router = APIRouter(
    tags=['CLIENT'],
)

admin_router = APIRouter(
    prefix='/admin',
    tags=['ADMIN'],
)

oauth_router = APIRouter(
    prefix='/oauth',
    tags=['OAUTH'],
)

file_router = APIRouter(
    prefix='/file',
    tags=['FILE'],
)

__all__ = [
    'client_router',
    'admin_router',
    'oauth_router',
    'file_router',
]
