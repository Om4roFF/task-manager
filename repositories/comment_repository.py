from typing import List

from db.comments import comments
from models.comment import *
from repositories.base import BaseRepository


class CommentRepository(BaseRepository):

    async def create(self, comment: CommentIn, user: User) -> Comment:
        now = datetime.utcnow()
        values = {**comment.dict(), 'created_at': now, 'updated_at': now}
        query = comments.insert().values(**values)
        comment_id = await self.database.execute(query)
        return Comment(id=comment_id,
                       created_at=now,
                       updated_at=now,
                       content=comment.content,
                       task_id=comment.task_id, user=user,)

    async def get_comments_by_task_id(self, task_id: int, user: User) -> List[Comment]:
        query = comments.select().where(comments.c.task_id == task_id).order_by(comments.c.id)
        items = await self.database.fetch_all(query)
        if items is None or len(items) == 0:
            return []
        fetched_comments = []
        for item in items:
            com = Comment.parse_obj(item)
            com.user = user
            fetched_comments.append(com)

        return fetched_comments
