from repositories.base import BaseRepository
from models.comments import Comment_base
import datetime
from db.comments import comments


class CommentRepositoryes(BaseRepository):

    async def create_job_comment(self, item: Comment_base) -> Comment_base:
        comment = Comment_base(
            id=0,
            job_uuid=item.job_uuid,
            comment=item.comment,
            performer_id=item.performer_id,
            is_publish=True,
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

