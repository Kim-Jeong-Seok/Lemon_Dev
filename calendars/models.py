from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
# Create your models here.




class Cardlist(models.Model):
    card_id = models.IntegerField(primary_key=True)
    card_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cardlist'

class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Spend(models.Model):
    spend_id = models.AutoField(primary_key=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    spend_date = models.DateTimeField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    way = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)
    card = models.ForeignKey(Cardlist, models.DO_NOTHING, db_column='card', blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spend'



class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    income_date = models.DateTimeField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    income_way = models.IntegerField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'income'




class AccountBook(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_date = models.DateTimeField(blank=True, null=True, auto_now_add = True)
    spend = models.ForeignKey('Spend', models.DO_NOTHING, blank=True, null=True)
    income = models.ForeignKey('Income', models.DO_NOTHING, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    kind = models.CharField(max_length=10, blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    way = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    card = models.CharField(max_length=20,blank=True, null=True)
    memo = models.TextField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'account_book'
