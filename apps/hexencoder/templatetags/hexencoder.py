import re

import codecs

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def convert_hex(string):
    hex_bytes = codecs.encode(bytes(string, 'utf-8'), 'hex')
    hex_str = hex_bytes.decode('utf-8')
    return hex_str


@register.simple_tag
def convert_hex_percent(string, regex=re.compile(r'(.{2})', re.DOTALL)):
    return regex.sub('%\\1', convert_hex(string), 0)


@register.simple_tag
def convert_hex_js(string):
    hex_str = convert_hex_percent(string)
    script_str = '<script type="text/javascript">document.write(unescape("{}"))</script>'.format(hex_str)
    return mark_safe(script_str)
