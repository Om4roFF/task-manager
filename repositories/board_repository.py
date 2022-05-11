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
        values.pop("tasks")
        values.pop("users")
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
        values.pop("tasks")
        values.pop("users")
        await self.database.execute(query, values=values)
        return item

    async def delete(self, board_id: int) -> bool:
        try:
            query = boards.delete().where(boards.c.id == board_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_board_by_group_id(self, group_id: int) -> Optional[Board]:
        query = boards.select().where(boards.c.group_id == group_id)
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        return Board.parse_obj(item)

    async def get_board_by__id(self, id: int) -> Optional[Board]:
        query = boards.select().where(boards.c.id == id)
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        return Board.parse_obj(item)

    async def delete_board(self, board_id):
        try:
            query = boards.delete().where(boards.c.id == board_id)
            await self.database.execute(query)
            return True
        except:
            return False
