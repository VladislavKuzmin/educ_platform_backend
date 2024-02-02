import uvicorn

from bootstrap import make_app  # noqa
from entities.course import Content
from settings import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        app=settings.server.ENTRYPOINT,
        host=settings.server.HOST,
        port=settings.server.PORT,
        server_header=False,
        proxy_headers=True,
        log_level='info',
        factory=True,
        workers=1,
    )


if __name__ == '__main__':
    main()
