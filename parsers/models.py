from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import declarative_base
from database import engine, SessionLocal

Base = declarative_base()


class ListingType(str, Enum):

    BUY = "BUY"
    SELL = "SELL"


class Listing(Base):
    """Модель сделки

    Args:
        external_id: id заявки внутри платформы
        datetime: Время получения заявки
        platform: Назавние платформы
        type: Тип сделки (BUY/SELL)
        amount: Сумма
        recipient_details: Реквизиты получателя
        currency: Валюта
        bank: Банк
        currency_rate: Курс валюты
        link: Ссылка на сделку на площадке

    """

    __tablename__ = "listings_listing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(Integer)
    datetime = Column(DateTime, nullable=False)
    platform = Column(String, nullable=False)
    type = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    recipient_details = Column(String, nullable=False)
    currency = Column(String, default="RUB")
    bank = Column(String, nullable=False)
    currency_rate = Column(Float, nullable=True)
    link = Column(String, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Listing(id={self.id}, type={self.type}, amount={self.amount}, "
            f"bank='{self.bank}', recipient='{self.recipient_details}')>"
        )


Base.metadata.create_all(bind=engine)
