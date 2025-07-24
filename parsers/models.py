from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from database import engine, SessionLocal

Base = declarative_base()

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

    external_id = Column()
    datetime = Column()
    platform = Column()
    type = Column()(choices=[("BUY", "buy"), ("SELL", "sell")], null=True)
    amount = Column()
    recipient_details = Column()  # Реквизит получателя
    currency = Column()
    bank = Column()
    currency_rate = Column()
    link = Column()

    def __repr__(self):
        return f"<Order(id={self.id}, external_id='{self.external_id}', account='{self.link}')>"


Base.metadata.create_all(bind=engine)
