import asyncio
from paylonium import PayloniumParser
import settings
import requests
from pydantic import BaseModel


def get_accounts():
    url = settings.BACKEND_URL + "/api/accounts"
    params = {"platform": 1}
    response = requests.get(url=url, params=params)
    print(response)
    try:
        data = response.json()
    except Exception as exc:
        raise exc
    return data


class Account(BaseModel):
    login: str
    password: str
    is_active: bool


def fabric_parsers() -> list[PayloniumParser]:
    accounts = get_accounts()
    parsers = []
    for account in accounts:
        account = Account(**account)
        if account.is_active:
            parser = PayloniumParser(
                account.login, password=account.password, account_name=account.login
            )
            parsers.append(parser)
        else:
            print(f"Аккаунт {account.login} неактивен, пропускаем.")
    return parsers


POLLING_INTERVAL_SECONDS = 10


async def worker(parser: PayloniumParser):
    """
    Задача-воркер, которая управляет одним экземпляром парсера.
    """
    print(f"Запускаю воркер для {parser.account_name}...")
    try:
        await parser.start()
        while True:
            await parser.fetch_and_save()
            print(
                f"[{parser.account_name}] Пауза на {POLLING_INTERVAL_SECONDS} секунд..."
            )
            await asyncio.sleep(POLLING_INTERVAL_SECONDS)

    except asyncio.CancelledError:
        print(f"Воркер для {parser.account_name} получил команду на остановку.")
    except Exception as e:
        print(
            f"Критическая ошибка в воркере для {parser.account_name}: {e}. Воркер остановлен."
        )
    finally:
        # 3. Корректное завершение: закрываем сессию
        await parser.stop()


async def main():
    parsers = fabric_parsers()
    if not parsers:
        print("Не найдено активных аккаунтов для запуска.")
        return

    tasks = [worker(p) for p in parsers]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершается по команде пользователя (Ctrl+C)...")
