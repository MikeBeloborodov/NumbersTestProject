
from pydantic import BaseModel
from datetime import datetime


class PostOrderRequest(BaseModel):
    order_id: int
    order_table_num: int
    order_num: int
    price_rub: float
    price_dollars: float
    delivery_date: datetime

    class Config:
        orm_mode = True