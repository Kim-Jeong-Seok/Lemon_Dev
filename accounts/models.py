from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class LemonUserManager(BaseUserManager):
    def create_user(self,uid, email, name,u_chk,e_chk,  invest, phonenumber, password=None):
        if not email:
            raise ValueError("이메일을 입력해주세요!")
        if not uid:
            raise ValueError("아이디를 입력해주세요!")
        if not name:
            raise ValueError("이름을 입력해주세요!")
        # if not balance:
        #     raise ValueError("월급을 입력해주세요!")
        if not invest:
            raise ValueError("모의자산을 입력해주세요!")
        if not phonenumber:
            raise ValueError("전화번호를 입력해주세요!")
        if not u_chk:
            raise ValueError("개인정보에 동의 해주세요!")
        if not e_chk:
            raise ValueError("이용약관에 동의 해주세요!")

        user = self.model(
            email = self.normalize_email(email),
            uid = uid,
            phonenumber = phonenumber,
            name = name,
            u_chk= u_chk,
            e_chk=e_chk,
            # balance = balance,
            invest = invest,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,uid, email,name, invest, phonenumber, password=None):
        user = self.create_user(
            uid = uid,
            email = email,
            phonenumber = phonenumber,
            name = name,
            u_chk = True,
            e_chk = True,
            invest = invest,
        )
        user.set_password(password)
    
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class user(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, db_collation='utf8_general_ci',verbose_name= "사용자이름")
    uid = models.CharField(unique=True, max_length=30, db_collation='utf8_general_ci', verbose_name= "유저아이디")
    password = models.CharField(max_length=30, db_collation='utf8_general_ci')
    email = models.CharField(unique=True, max_length=15, db_collation='utf8_general_ci', verbose_name= "이메일")
    phonenumber = models.CharField(unique=True, max_length=15, db_collation='utf8_general_ci', blank=True, null=True,verbose_name= "전화번호")
    invest = models.IntegerField(verbose_name="모의투자금",blank=True, null=True)
    invest_date = models.DateTimeField(verbose_name="투자금액설정일",blank=True, null=True)
    u_chk = models.BooleanField(verbose_name="개인정보 동의체크",blank=True, null=True, default = 0)
    e_chk = models.BooleanField(verbose_name="개인정보 동의체크",blank=True, null=True, default = 0)
    o_chk = models.BooleanField(verbose_name="회원탈퇴 여부",blank=True, null=True, default = 1 )
    status = models.IntegerField(verbose_name="회원상태",blank=True, null=True, default = 0 )
    join_date = models.DateTimeField(verbose_name="가입날",blank=True, null=True, auto_now_add = True)
    balance = models.IntegerField(verbose_name="잔고",blank=True, null=True)
    last_login = models.DateTimeField(verbose_name= "최근 로그인 날짜",blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['email','name','phonenumber','invest']
    objects=LemonUserManager()
    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return self.uid

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    
    
class AccountBook(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_date = models.DateTimeField(blank=True, null=True)
    spend = models.ForeignKey('Spend', models.DO_NOTHING, blank=True, null=True)
    income = models.ForeignKey('Income', models.DO_NOTHING, blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_book'


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
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

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
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'income'