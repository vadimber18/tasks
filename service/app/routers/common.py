from typing import Optional

MAX_LIMIT = 100


class CommonPaginationParams:
    def __init__(self, limit: Optional[int] = 10, offset: Optional[int] = 0):
        self.limit = limit if limit <= MAX_LIMIT else MAX_LIMIT
        self.offset = offset
