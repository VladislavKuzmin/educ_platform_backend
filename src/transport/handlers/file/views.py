from services.file import upload_file, get_file

from transport.handlers.file.schemas import GetFileRequestSchema
from transport.routers import file_router

from fastapi import UploadFile, Depends
from fastapi.responses import StreamingResponse

from settings import FILES_PATH


@file_router.get(
    path='/',
    summary='Получение файла',
)
async def get_file_view(
    request: GetFileRequestSchema = Depends(),
):
    if not (file := await get_file(id=request.id)):
        return None

    file_path = FILES_PATH.joinpath(f"{file.id}.{file.extension}")

    def iterfile():  #
        with open(file_path, mode="rb") as file_like:  #
            yield from file_like  #

    return StreamingResponse(
        iterfile(),
        media_type='video/*'
    )


@file_router.post(
    path='/',
    summary='Загрузка файла',
)
async def upload_file_view(
        file: UploadFile,
):
    return await upload_file(
        content=await file.read(),
        extension=file.filename.split('.')[-1]
    )
