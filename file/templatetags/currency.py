from django import template
import decimal
from django.http import HttpResponse
from decimal import Decimal, DecimalException
import locale

register = template.Library()

@register.filter
def currency_converter(amount): # Only one argument.
    """Converts a Amount to the US  Currency with Input html"""
    if amount.value():
  
        locale.setlocale(locale.LC_ALL,'')    
        
        s = """<input type="text" name="{}" class="calculate_ltv form-control" placeholder="Enter value" value="{}" maxlength="50" id="{}">""".format(
            amount.name, locale.currency( float(amount.value()), grouping=True, symbol=False), amount.auto_id 
        )
        return s
    return amount

@register.filter
def currency_form_converter(amount): # Only one argument.
    """Converts a Amount to the US  Currency with only value"""
    try:
        if amount:
            locale.setlocale(locale.LC_ALL,'')    
            s = locale.currency( float(amount), grouping=True, symbol=False)
            return s
        return amount
    except Exception:
        return amount

@register.filter
def convert_to_int(value):
    """convert string to int."""
    try:
        state_id = int(value)
    except Exception:
        state_id = value
    return state_id

@register.simple_tag
def expenses_addtion(bw_value, **kwargs):
    """Add the expense information"""
    try:
        borrower = 0
        if bw_value:
            borrower = float(bw_value)

        s = []

        for i in kwargs['cw_values']:
            if kwargs['specified_field'] == 'monthly_income':
                key_value = i.monthly_income
            elif kwargs['specified_field'] == 'net_rental_income':
                key_value = i.net_rental_income
            elif kwargs['specified_field'] == 'overtime':
                key_value = i.overtime
            elif kwargs['specified_field'] == 'bonuses':
                key_value = i.bonuses
            elif kwargs['specified_field'] == 'commissions':
                key_value = i.commissions
            elif kwargs['specified_field'] == 'dividends_interest':
                key_value = i.dividends_interest
            elif kwargs['specified_field'] == 'other':
                key_value = i.other
            
            if key_value is None or len(key_value)<0:
                a = 0
            else:
                a = float(key_value)
            s.append(a)
        total = 0
        ele = 0
        # Iterate each element in list 
        # and add them in variale total 
        while(ele < len(s)): 
            total = total + s[ele]
            ele += 1

        total = borrower + total
    except Exception as e:      
        total = 0
    return total

@register.filter
def check_none_values(value):
    """convert string to int."""
    if value is None or len(value)<0:
        return ''
    elif value == 'None':
        return ''
    return value

@register.filter
def file_extension_remove(value):
    """convert string to int."""
    try:
        extension_remove = str(value).split('.')[0]
    except Exception:
        return value
    return extension_remove