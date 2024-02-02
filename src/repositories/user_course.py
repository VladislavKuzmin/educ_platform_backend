from entities.user_course import UserCourseEntity
from repositories.models.user_courses import UserCourseDBModel
from repositories.base import MongoDBRepositoryBase


class UserCourseRepository(
    MongoDBRepositoryBase,
):
    _COLLECTION_NAME = 'user_course'
    _COLLECTION_MODEL = UserCourseDBModel

    async def update_with_push(
            self,
            obj: UserCourseEntity,
    ) -> None:
        query = {"course_id": obj.course_id, "user_id": obj.user_id}
        update_query = {"$push": {}, "$set": {}}

        for key, value in obj.model_dump(exclude_unset=True, exclude_defaults=True, exclude={
            'id': True,
            'user_id': True,
            'course_id': True
        }).items():
            if isinstance(value, list):
                update_query["$push"].update({key: {"$each": value}})
            else:
                update_query["$set"].update({key: value})

        await self._collection.update_one(query, update_query)
