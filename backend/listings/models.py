from django.db import models


class Listing(models.Model):
    external_id = models.IntegerField()
    datetime = models.DateTimeField()
    platform = models.CharField()  # Возможно сделать отдельную модель под площадку
    type = models.CharField(choices=[("BUY", "buy"), ("SELL", "sell")])
    amount = models.FloatField()
    recipient_details = models.CharField()  # Реквизит получателя
    currency = models.CharField()
    bank = models.CharField()
    currency_rate = models.FloatField(null=True)
    link = models.CharField()

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
