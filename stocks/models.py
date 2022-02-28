from django.db import models
from django.conf import settings


# Create your models here.
class Stockheld(models.Model):
    sh_id = models.AutoField(db_column='sh_Id', primary_key=True)
    sh_userid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='sh_userId')
    sh_isusrtcd = models.CharField(db_column='sh_isuSrtCd', max_length=10)
    sh_isucd = models.CharField(db_column='sh_isuCd', max_length=30, blank=True, null=True)
    sh_isukorabbrv = models.CharField(db_column='sh_isuKorAbbrv', max_length=30)
    sh_marketcode = models.CharField(max_length=20)
    sh_idxindmidclsscd = models.CharField(db_column='sh_idxIndMidclssCd', max_length=20)
    sh_share = models.IntegerField()
    sh_price = models.IntegerField()
    sh_z_date = models.DateTimeField()
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


class Stockprofit(models.Model):
    sp_userid = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='sp_userId', primary_key=True)  # Field name made lowercase.
    sp_profit = models.IntegerField()
    sp_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'stockprofit'


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


class Totalmerge(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=50)
    marketcode = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    per = models.SmallIntegerField()
    pbr = models.SmallIntegerField()
    haltyn = models.CharField(db_column='haltYN', max_length=5)  # Field name made lowercase.
    logo = models.CharField(max_length=70)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'TotalMerge'

class bookmark(models.Model):
    Bookmark_id= models.AutoField(db_column='Bookmark_id', primary_key=True)
    user_id = models.CharField(max_length=20)
    marketcode = models.CharField(max_length=20)
    isuSrtCd = models.CharField(db_column='ss_isuSrtCd', max_length=30, blank=True, null=True)
    activate = models.CharField(max_length=2)
    class Meta:
        managed = False
        db_table = 'bookmark'

#나스닥 테스트용


class nasdaq_category(models.Model):
    idnasdaq_num = models.AutoField(db_column='idnasdaq_num', primary_key=True)
    category = models.OneToOneField(
    Totalmerge, models.DO_NOTHING, db_column='category', blank=True, null=True)
    nasdaq_cname = models.CharField(max_length=50)
    Kor = models.CharField(max_length=50)
    marketcode = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'nasdaq_category'
