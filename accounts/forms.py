from django import forms
from .models import user, Spend, Income

class LemonSignupForm(forms.Form):
    uid = forms.CharField()
    password = forms.CharField()
    email = forms.CharField()
    name = forms.CharField()
    phonenumber = forms.CharField()
    money = forms.CharField()
    fakemoney = forms.CharField()
    moneydate = forms.DateTimeField()
    

class SpendForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = ['user','kind','spend_date','amount','place', 'way', 'category', 'card', 'memo']
        
        
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['user','kind','income_date','amount','income_way','memo']
