from django.db import models
from django.conf import settings


# Create your models here.


class TotalMerge(models.Model):
    id = models.CharField(db_column='id', primary_key=True,max_length=30)
    name = models.CharField(db_column='name', max_length=30)
    market_code = models.CharField(db_column='market_code', max_length=30, blank=True, null=True)
    category = models.IntegerField(db_column='category')
    ss_haltyn = models.CharField(db_column='ss_haltYN', max_length=5)
    logo = models.CharField(db_column='logo', max_length=20)
    date = models.DateTimeField(db_column='date',auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'TotalMerge'





class Stockheld(models.Model):
    sh_id = models.AutoField(db_column='sh_Id', primary_key=True)
    sh_userid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='sh_userId')
    sh_isusrtcd = models.CharField(db_column='sh_isuSrtCd', max_length=10)
    sh_isucd = models.CharField(db_column='sh_isuCd', max_length=30, blank=True, null=True)
    sh_isukorabbrv = models.CharField(db_column='sh_isuKorAbbrv', max_length=30)
    sh_marketcode = models.CharField(max_length=20)
    sh_idxindmidclsscd = models.CharField(db_column='sh_idxIndMidclssCd', max_length=20)
    sh_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'stockheld'


class Stocktrading(models.Model):
    st_id = models.AutoField(primary_key=True)
    st_userid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='st_userId')
    st_isusrtcd = models.CharField(db_column='st_isuSrtCd', max_length=30)
    st_kind = models.CharField(max_length=5)
    st_share = models.SmallIntegerField()
    st_price = models.IntegerField()
    st_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'stocktrading'


class Stocksector(models.Model):
    ss_isusrtcd = models.CharField(db_column='ss_isuSrtCd', primary_key=True, max_length=30)
    ss_isukorabbrv = models.CharField(db_column='ss_isuKorAbbrv', max_length=30, blank=True, null=True)
    ss_marketcode = models.CharField(max_length=30)
    ss_idxindmidclsscd = models.CharField(db_column='ss_idxIndMidclssCd', max_length=30, blank=True, null=True)
    ss_haltyn = models.CharField(db_column='ss_haltYN', max_length=5)
    ss_logo = models.CharField(max_length=70, blank=True, null=True)
    ss_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'stocksector'


class Stockclass(models.Model):
    sc_id = models.AutoField(primary_key=True)
    sc_marketcode = models.CharField(max_length=8)
    sc_idxindmidclsscd = models.CharField(db_column='sc_idxIndMidclssCd', max_length=8)
    sc_class = models.CharField(max_length=20)
    sc_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'stockclass'
