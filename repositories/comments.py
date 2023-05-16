from repositories.base import BaseRepository
from models.comments import Comment_base, Comment_model_in
import datetime
from db.comments import comments
from db.jobs import jobs, active_jobs, booking_job
from db.users import users
from sqlalchemy import select, desc


class CommentRepositoryes(BaseRepository):

    async def create_job_comment(self, item: Comment_model_in) -> Comment_base:
        # коммент создается исполнителем джобы
        comment = Comment_base(
            id=0,
            job_uuid=item.job_uuid,
            comment=item.comment,
            author_id=item.author_id,
            performer_id=item.performer_id,
            is_publish=True,
            is_author_read=True, #для автора есть сообщение
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()

        )
        values = {**comment.dict()}
        values.pop("id", None)
        query = comments.insert().values(**values)
        comment.id = await self.database.execute(query=query)
        if comment is None:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="phone not found")
            return False
        return comment

    async def get_comment_by_performer_id(self, performer_id: int):
        # достать строчки исполнителя с id = performer_id
        query = select(comments, jobs, users).where(comments.c.performer_id == performer_id).join(jobs,
                                                                                                  comments.c.job_uuid == jobs.c.uuid).join(
            users, jobs.c.user_id == users.c.id).order_by(desc(comments.c.updated_at))
        result = await self.database.fetch_all(query=query)
        if result is None:
            return False
        return result

    async def get_comment_by_author_id(self, author_id: int):
        # достать строчки исполнителя с id = author_id
        query = select(comments, jobs, users).where(comments.c.author_id == author_id).join(jobs,
                                                                                            comments.c.job_uuid == jobs.c.uuid).join(
            users, comments.c.performer_id == users.c.id).order_by(desc(comments.c.updated_at))
        result = await self.database.fetch_all(query=query)
        if result is None:
            return False
        return result

    async def set_is_author_read(self, comment_id):
        query = comments.update().where(comments.c.id == comment_id).values(is_author_read=False)
        try:
            await self.database.execute(query)
            return True
        except Exception as e:
            print(f'set_is_author_read---> {e}')
            return False

    async def set_is_performer_read(self, comment_id):
        query = comments.update().where(comments.c.id == comment_id).values(is_performer_read=False)
        try:
            await self.database.execute(query)
            return True
        except Exception as e:
            print(f'set_is_performer_read---> {e}')
            return False
