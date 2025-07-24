import asyncio
from paylonium import PayloniumParser
import settings
import requests


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


def fabric_parsers():
    accounts = get_accounts()
    print(accounts)
    parsers = []
    for account in accounts:
        parser = PayloniumParser(
            account.login, password=account.password, account_name=account.login
        )
        parsers.append(parser)


async def main():
    fabric_parsers()


if __name__ == "__main__":
    asyncio.run(main())
