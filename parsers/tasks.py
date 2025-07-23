from celery import shared_task
from .models import ParserAccount
from .tasks import run_parser_for_account
from celery import shared_task
from .registry import PARSER_REGISTRY
from .models import ParserAccount
from listings.services import save_parsed_order


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def run_parser(self, account_id: int):
    account = ParserAccount.objects.get(pk=account_id)
    ParserCls = PARSER_REGISTRY[account.parser_type]
    parser = ParserCls(account.login, account.password, account.account_name, account.telegram_id)
    
    parser.authenticate()
    orders = parser.get_new_orders()
    
    for order in orders:
        save_parsed_order(order, source=account.parser_type, account_name=account.account_name)

@shared_task
def schedule_all_parsers():
    for acc in ParserAccount.objects.filter(is_enabled=True):
        run_parser_for_account.delay(acc.id)
