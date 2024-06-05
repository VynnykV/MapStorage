from enum import Enum
from typing import Tuple, Optional, TypeVar, Any

from pydantic import BaseModel, conint, constr
from sqlalchemy import select, Select, desc

T = TypeVar('T')


class OrderByDirection(str, Enum):
    asc = 'asc'
    desc = 'desc'


class FilteredQuery(BaseModel):
    offset: conint(ge=0) = 0
    limit: conint(ge=1, le=500) = 10
    order_by: Tuple[str, OrderByDirection] = ()
    search_str: Optional[constr(min_length=1, strip_whitespace=True)] = None

    def db_query(self, entity: Any) -> Select:
        query = self.filter_by(select(entity))

        for criteria in self.order_by:
            query = query.order_by(criteria[0]) if criteria[1] == 'asc' \
                    else query.order_by(desc(criteria[0]))

        query = query.offset(self.offset).limit(self.limit)

        return query

    def filter_by(self, select_expression: Select) -> Select:
        return select_expression.where()
