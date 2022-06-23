from database_logic import Base
from sqlalchemy import Column, Integer, Float, String


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    order_table_num = Column(String)
    order_num = Column(String)
    price_rub = Column(Float)
    price_usd = Column(Float)
    delivery_date = Column(String)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
