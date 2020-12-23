import markdown
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown_to_html(text):
    """ マークダウンをhtmlに変換する。
    https://python-markdown.github.io/reference/#extensions
    このfilterでhtml表示する場合、bulmaではclass='content'が必要。
    """
    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)
