from django import forms

from .models import Spend, Income

class SpendForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = ['user','kind','spend_date','amount','place', 'way', 'category', 'card', 'memo']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['user','kind','income_date','amount','income_way','memo']
