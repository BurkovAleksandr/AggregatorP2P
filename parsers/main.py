import asyncio
from paylonium import PayloniumParser


def fabric_parsers():
    accounts = get_accounts()
    parsers = []
    for account in accounts:
        parser = PayloniumParser(account.login, password=account.password, account_name=account.login)


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
