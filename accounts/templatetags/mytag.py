from django import template

register = template.Library()


# 쿼리셋 비교하여 day에 일치하는 money값 return
@register.filter
def find_spend_money(queryset, day):
    for item in queryset:
        if day == item['spend_date__day']:
            return item['amount']


@register.filter
def find_income_money(queryset, day):
    for item in queryset:
        if day == item['income_date__day']:
            return item['amount']


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def rounds(value, arg):
    return round(value, arg)
# @register.filter
# def divs(value , arg):
#     if arg:
#         return value / arg
#     else:
#         return 0


# def div(value, arg):
#     """Divide the arg by the value."""
#     try:
#         nvalue, narg = handle_float_decimal_combinations(
#             valid_numeric(value), valid_numeric(arg), '/')
#         return nvalue / narg
#     except (ValueError, TypeError):
#         try:
#             return value / arg
#         except Exception:
#             return 0

@register.filter
def yields(value, arg):
    if arg:
        return (value - arg) * 100 / arg
    else:
        return float('0')
