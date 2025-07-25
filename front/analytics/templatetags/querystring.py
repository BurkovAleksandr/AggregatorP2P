from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Возвращает строку query-параметров, где page подменяется, а все остальные сохраняются.
    Пример использования:
        {% query_transform page=2 %}
    """
    query = context["request"].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return "?" + query.urlencode()
