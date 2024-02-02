from typing import Annotated
from urllib.parse import quote

from authlib.integrations.base_client import OAuthError
from fastapi import Depends, Request
from pydantic import ValidationError
from starlette.responses import RedirectResponse

from entities.user import UserEntity
from exceptions.auth import GoogleOAuthError
from services.data_types import GoogleToken
from services.user import get_user_service, create_user_service
from settings import get_settings
from transport.routers import oauth_router
from utils import AppState, get_app_state


@oauth_router.get("/google_login")
async def google_login(
        request: Request,
        app_state: Annotated[AppState, Depends(get_app_state)]
) -> RedirectResponse:
    request.session.clear()
    return await app_state.oauth.google.authorize_redirect(request, get_settings().google_oauth.REDIRECT_URI)


@oauth_router.get("/callback")
async def login_callback_view(
        request: Request,
        app_state: Annotated[AppState, Depends(get_app_state)]
) -> RedirectResponse:
    try:
        token = GoogleToken.model_validate(await app_state.oauth.google.authorize_access_token(request))
    except (OAuthError, ValidationError) as error:
        raise GoogleOAuthError from error

    if not (user_entity := await get_user_service(identifier=token.userinfo.email, identifier_field='email')):
        user_entity = UserEntity.from_google_oauth_token(token)
        user_entity = await create_user_service(user_entity)

    request.session['user'] = user_entity.model_dump(exclude={'created_at'})
    return RedirectResponse(url=f'{app_state.settings.frontend.AUTH_REDIRECT_URL}?user_id={quote(user_entity.id)}')


@oauth_router.get('/logout')
async def logout(request: Request, app_state: Annotated[AppState, Depends(get_app_state)]):
    request.session.pop('user', None)
    return RedirectResponse(url=f'http://{app_state.settings.frontend.HOST}:{app_state.settings.frontend.PORT}')

