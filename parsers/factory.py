from django.utils.module_loading import import_string

from parsers.models import ParserAccount


def get_parser_instance(account: ParserAccount):
    parser_path = account.platform.parser_class
    ParserClass = import_string(parser_path)
    return ParserClass(
        login=account.login,
        password=account.password,
    )
