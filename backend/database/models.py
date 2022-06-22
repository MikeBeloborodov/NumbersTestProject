from database_logic import Base
from sqlalchemy import Column, Integer, Date, Float


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    order_table_num = Column(Integer, nullable=False)
    order_num = Column(Integer, nullable=False)
    price_rub = Column(Float, nullable=False)
    price_usd = Column(Float, nullable=False)
    delivery_date = Column(Date, nullable=False)
