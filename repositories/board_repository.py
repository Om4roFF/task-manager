from datetime import datetime
from typing import Optional

from db import boards
from models.board import Board
from repositories.base import BaseRepository


class BoardRepository(BaseRepository):

    async def create(self, board: Board) -> Board:
        now = datetime.utcnow()
        item = Board(created_at=now, updated_at=now, description=board.description, group_id=board.group_id)
        values = {**item.dict()}
        values.pop("id", None)
        query = boards.insert().values(**values)
        item.id = await self.database.execute(query)
        return item

    async def update(self, board: Board) -> Optional[Board]:
        now = datetime.utcnow()
        item = Board(created_at=now, updated_at=now, description=board.description, group_id=board.group_id,
                     id=board.id)
        if item.id is None:
            return None
        query = boards.update().where(boards.c.id == board.id)
        values = {**item.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        await self.database.execute(query, values=values)
        return item

    async def delete(self, board_id: int) -> bool:
        try:
            query = boards.delete().where(boards.c.id == board_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_board_by_id(self, user_id: int):
        # query = boards.select().where()
        pass