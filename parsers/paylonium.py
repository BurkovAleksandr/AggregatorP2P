import functools
import json
import os
import pickle
import time
from typing import List
import aiohttp
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import re
from base import BaseParser
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from models import Listing, ListingType
import settings
from sqlalchemy.orm import sessionmaker
from database import engine  # здесь у тебя должен быть engine

Session = sessionmaker(bind=engine)
db_session = Session()
# URL для входа и для получения заявок
LOGIN_URL = "https://profile.paylonium.com/login"
GET_ORDERS_URL = os.getenv("GET_ORDERS_URL")
ParsedOrder = namedtuple(
    "ParsedOrder", ["paylonium_id", "datetime", "bank", "amount", "recipient_details"]
)


class PayloniumParser(BaseParser):
    def __init__(self, login, password, account_name):
        self._login = login
        self._password = password
        self.account_name = account_name
        self.cookie_jar = aiohttp.CookieJar(unsafe=True)
        self.session = aiohttp.ClientSession(cookie_jar=self.cookie_jar)
        self.cookie_path = os.path.join(
            settings.SESSIONS_PATH,
            f"{self.safe_filename(self.account_name)}.cookies",
        )
        self.session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "DNT": "1",
                "Host": "profile.paylonium.com",
                "Origin": "https://profile.paylonium.com",
                "Pragma": "no-cache",
                "Referer": "https://profile.paylonium.com/p/getnew",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "TE": "trailers",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
            }
        )
        self._is_authenticated = False

    def parse_auth_data(self, response: str):
        """Парсит ответ запроса авторизации

        Args:
            auth_data (str): HTML страничка ответа

        Raises:
            Exception: Возвращает базовый Exception с текстом "Неверное имя/пароль"

        Returns:
            bool: Возвращает True если все хорошо, и выкидывает исключение если все плохо
        """
        soup = BeautifulSoup(response, "lxml")
        alert = soup.find("div", class_="alert callout")
        if alert and alert.getText().strip() == "Неверное имя/пароль":
            raise Exception("Неверное имя/пароль")
        else:
            return True

    async def login(self):
        """Выполняет вход в систему и сохраняет сессию."""
        if await self.load_session():
            return

        print(f"Выполняю авторизацию для {self._login}")
        login_data = {
            "username": self._login,
            "password": self._password,
        }

        response = await self.session.post(
            LOGIN_URL, data=login_data, allow_redirects=True
        )
        response.raise_for_status()  # Если статус не 200 кидает HTTPError
        html = await response.text()
        self.parse_auth_data(
            html
        )  # Если в контенте страницы есть ошибка выкидывает Exception
        self._is_authenticated = True
        self.save_session()

    def require_auth(self):
        """Проверка авторизации

        Raises:
            Exception: Возвращает базовый Exception с текстом "Autentification required"
        """
        if not self._is_authenticated:
            raise Exception("Authentication required")

    def safe_filename(self, name: str) -> str:
        """Удаляет опасные символы из имени файла"""
        return re.sub(r"[^A-Za-z0-9_.-]", "_", name)

    def save_session(self):
        """Сохранение сессии"""
        self.cookie_jar.save(
            self.cookie_path,
        )

    async def load_session(self):
        """Загрузка сессии

        Returns:
            bool: True если успех, False - если провал
        """

        if os.path.exists(self.cookie_path):
            try:
                self.session.cookie_jar.load(self.cookie_path)
                if await self.check_session():
                    print(f"[{self.account_name}] Сессия успешно загружена.")
                    self._is_authenticated = True
                    return True
                else:
                    print(f"[{self.account_name}] Сессия невалидна.")
            except Exception as e:
                print(f"[{self.account_name}] Ошибка при загрузке сессии: {e}")
        return False

    async def check_session(self):
        response = await self.session.get(GET_ORDERS_URL, allow_redirects=False)
        # response.raise_for_status()
        if response.status == 200 and "login" not in str(response.url):
            return True
        return False

    def _parse_orders_data(self, data: str):

        soup = BeautifulSoup(data, "lxml")
        orders = []

        order_rows = (
            soup.find("table", {"class": "report_table p2p_new"})
            .find("tbody")
            .find_all("tr")
        )

        for row in order_rows:
            cols = row.find_all("td")
            if not cols:
                continue
            pl_id = cols[0].text.strip()
            dt_str = cols[1].text.strip()  # '2025-06-06 18:11:16'
            bank_img = cols[2].find("img")
            bank = bank_img["alt"].strip() if bank_img else cols[2].text.strip()
            amount_str = cols[3].text.replace(",", ".")
            amount = float(amount_str)
            recipient = cols[4].text.strip()

            orders.append(
                ParsedOrder(
                    paylonium_id=pl_id,
                    datetime=dt_str,
                    bank=bank,
                    amount=amount,
                    recipient_details=recipient,
                )
            )
        return orders

    async def get_new_orders(self) -> List[ParsedOrder]:
        """Получает новые заявки с сайта

        Returns:
            List[ParsedOrder]: Список заявок
        """
        self.require_auth()
        try:
            response = await self.session.get(GET_ORDERS_URL)
            if response.status == 401 or "login" in str(response.url):
                print(f"[{self.account_name}] Сессия истекла, переавторизация...")
                self._is_authenticated = False
                await self.login()
                response = await self.session.get(GET_ORDERS_URL)

            response.raise_for_status()
            html = await response.text()
            # with open("getnew.htm", "r", encoding="utf-8") as f:
            #     html = f.read()
            return self._parse_orders_data(html)

        except aiohttp.ClientError as e:
            print(f"[{self.account_name}] Ошибка сети: {e}")
            return []
        except Exception as e:
            print(f"[{self.account_name}] Ошибка парсинга: {e}")
            with open(f"debug_{time.time()}.html", "w", encoding="utf-8") as f:
                f.write(await response.text())
            return []

    def save_listing(self, parsed_order: ParsedOrder):
        data = {
            "external_id": parsed_order.paylonium_id,
            "datetime": parsed_order.datetime,
            "platform": "paylonium",
            "type": "BUY",
            "amount": parsed_order.amount,
            "recipient_details": parsed_order.recipient_details,
            "bank": parsed_order.bank,
            "link": "example",
        }

        # Логируем для отладки
        with open("res.json", "a") as f:
            json.dump(data, fp=f)
            f.write("\n")
        print(data)

        try:
            existing = (
                db_session.query(Listing)
                .filter_by(
                    external_id=parsed_order.paylonium_id,
                    platform="paylonium",
                )
                .one_or_none()
            )

            if existing:
                # Обновляем существующую заявку
                existing.datetime = parsed_order.datetime
                existing.type = ListingType("BUY")
                existing.amount = parsed_order.amount
                existing.recipient_details = parsed_order.recipient_details
                existing.bank = parsed_order.bank
                existing.link = "example"
            else:
                # Создаём новую
                listing = Listing(
                    external_id=parsed_order.paylonium_id,
                    datetime=parsed_order.datetime,
                    platform="paylonium",
                    type=ListingType("BUY"),
                    amount=parsed_order.amount,
                    recipient_details=parsed_order.recipient_details,
                    bank=parsed_order.bank,
                    link="example",
                )
                db_session.add(listing)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Ошибка при сохранении заявки: {e}")

    async def start(self):
        """Выполняет вход и подготавливает сессию."""
        try:
            await self.login()
        except Exception as e:
            print(f"[{self.account_name}] Ошибка во время первоначального входа: {e}")
            raise  # Пробрасываем ошибку выше, чтобы задача-worker не запустилась

    async def stop(self):
        """Закрывает сессию."""
        if self.session and not self.session.closed:
            await self.session.close()
            print(f"[{self.account_name}] Сессия закрыта.")

    async def fetch_and_save(self):
        """
        Выполняет один цикл получения и сохранения заявок.
        Предполагается, что логин уже выполнен.
        """
        try:
            listings = await self.get_new_orders()
            for listing in listings:
                self.save_listing(listing)
            # Если заявок нет, можно вывести сообщение
            if not listings:
                print(f"[{self.account_name}] Новых заявок не найдено.")
        except Exception as e:
            # Логируем ошибку, но не останавливаем весь цикл.
            # Возможно, это временная проблема с сетью или сайтом.
            print(f"[{self.account_name}] Ошибка в цикле получения данных: {e}")
