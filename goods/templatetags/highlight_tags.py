from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()


@register.filter
def highlight(text, keyword):
    """将文本中的关键词用 <mark> 标签包裹高亮（不区分大小写）"""
    if not keyword or not text:
        return text
    escaped = escape(str(text))
    pattern = re.compile(re.escape(escape(keyword)), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda m: f'<mark class="bg-yellow-200 text-yellow-900 rounded px-0.5">{m.group()}</mark>',
        escaped
    )
    return mark_safe(highlighted)
