from django import template
import decimal
from django.http import HttpResponse
from decimal import Decimal, DecimalException
import locale
import mimetypes    

register = template.Library()

@register.filter
def filetype(url): # Only one argument.
    file_type = mimetypes.guess_type(url,strict = True)
    return file_type