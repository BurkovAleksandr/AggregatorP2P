

from celery import shared_task
from parsers.factory import get_parser_instance
from parsers.models import ParserAccount, Platform


@shared_task
def run_platform_parsers():
    for platform in Platform.objects.filter(is_active=True):
        parse_all_accounts_for_platform.delay(platform.code)


@shared_task
def parse_all_accounts_for_platform(platform_code):
    platform = Platform.objects.get(code=platform_code)
    accounts = ParserAccount.objects.filter(platform=platform, is_active=True)

    for acc in accounts:
        run_account_parser.delay(acc.id)


@shared_task
def run_account_parser(account_id):
    account = ParserAccount.objects.select_related("platform").get(id=account_id)

    parser = get_parser_instance(account)

    if not parser.is_logged_in():
        parser.login()

    listings = parser.fetch_listings()
    save_listings_to_db(account, listings)