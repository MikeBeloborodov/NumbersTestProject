from database_logic import Base
from sqlalchemy import Column, Integer, Date


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    order_table_num = Column(Integer, nullable=False)
    price_rub = Column(Integer, nullable=False)
    price_dollars = Column(Integer, nullable=False)
    delivery_date = Column(Date, nullable=False)
