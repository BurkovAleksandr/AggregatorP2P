from django.db import models


class Platform(models.Model):
    name = models.CharField("Название", max_length=50)
    code = models.CharField("Кодовое название", max_length=50)


class Listing(models.Model):
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

    external_id = models.CharField()
    datetime = models.DateTimeField()
    platform = models.CharField()
    type = models.CharField(choices=[("BUY", "buy"), ("SELL", "sell")], null=True)
    amount = models.FloatField()
    recipient_details = models.CharField()  # Реквизит получателя
    currency = models.CharField(null=True)
    bank = models.CharField()
    currency_rate = models.FloatField(null=True)
    link = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_external_id",
                fields=["external_id"],
            )
        ]

    def __repr__(self):
        return f"<Order(id={self.id}, external_id='{self.external_id}', account='{self.link}')>"


# ○	ID заявки
# ○	Дата-время получения / передачи исполнителю
# ○	Биржа / площадка
# ○	Тип: BUY / SELL
# ○	Сумма
# ○	Получатель (реквизит)
# ○	Валюта
# ○	Платёжная система / банк
# ○	Цена (курс) (если есть)
# ○	Линк на сделку / профиль трейдера
