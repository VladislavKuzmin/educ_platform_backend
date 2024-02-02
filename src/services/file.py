from entities.file import FileEntity
from repositories.file import FileRepository
from settings import FILES_PATH

import aiofiles


async def upload_file(content, extension: str) -> str:
    file_repo = await FileRepository.get_repository()
    new_file = await file_repo.create(FileEntity(extension=extension))

    file_path = FILES_PATH.joinpath(f"{new_file.inserted_id}.{extension}")
    async with aiofiles.open(file_path, 'wb+') as f:
        await f.write(content)

    return new_file.inserted_id


async def get_file(id: str):
    file_repo = await FileRepository.get_repository()
    file = await file_repo.read_by_id(id)
    if not file:
        return None
    return file
