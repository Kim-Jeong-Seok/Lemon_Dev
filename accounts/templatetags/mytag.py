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