from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import datetime

# Create your models here.
class LemonUserManager(BaseUserManager):
    def create_user(self, uid, pin, pin_date, gender, job, birthday, email, username, u_chk,  invest, invest_date, phonenumber, password=None):
        if not email:
            raise ValueError("이메일을 입력해주세요!")
        if not uid:
            raise ValueError("아이디를 입력해주세요!")
        if not username:
            raise ValueError("이름을 입력해주세요!")
        if not u_chk:
            raise ValueError("개인정보에 동의 해주세요!")


        user = self.model(
            email = self.normalize_email(email),
            uid = uid,
            phonenumber = phonenumber,
            username = username,
            u_chk= u_chk,
            invest = invest,
            invest_date=invest_date,
            gender = gender,
            job = job,
            birthday= birthday,
            pin = pin,
            pin_date = pin_date,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,uid, email,username, phonenumber, password=None):
        user = self.create_user(
            uid = uid,
            email = email,
            phonenumber = phonenumber,
            username = username,
            u_chk = True,
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
    username = models.CharField(max_length=30, db_collation='utf8_general_ci',verbose_name= "사용자이름")
    uid = models.CharField(unique=True, max_length=30, db_collation='utf8_general_ci', verbose_name= "유저아이디")
    password = models.CharField(max_length=30, db_collation='utf8_general_ci')
    email = models.CharField(unique=True, max_length=100, db_collation='utf8_general_ci', verbose_name= "이메일")
    phonenumber = models.CharField(unique=True, max_length=24, db_collation='utf8_general_ci', blank=True, null=True,verbose_name= "전화번호")
    invest = models.IntegerField(verbose_name="모의투자금",blank=True, null=True, default=0)
    invest_date = models.DateField(verbose_name="투자금액설정일",blank=True, null=True)
    u_chk = models.BooleanField(verbose_name="개인정보 동의체크",blank=True, null=True, default = 0)
    o_chk = models.BooleanField(verbose_name="회원탈퇴 여부",blank=True, null=True, default = 1 )
    status = models.IntegerField(verbose_name="회원상태",blank=True, null=True, default = 0 )
    join_date = models.DateTimeField(verbose_name="가입날",blank=True, null=True, auto_now_add = True)
    balance = models.IntegerField(verbose_name="잔고",blank=True, null=True)
    last_login = models.DateTimeField(verbose_name= "최근 로그인 날짜",blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    pin = models.CharField(verbose_name="pin번호", blank=True, null=True, max_length=8)
    gender = models.CharField(max_length=10, db_collation='utf8_general_ci', verbose_name= "성별")
    job = models.IntegerField(verbose_name="직업",blank=True, null=True)
    birthday = models.DateTimeField(verbose_name="생년월일",blank=True, null=True)
    pin_date = models.DateTimeField(verbose_name="핀입력시간",blank=True, null=True)


    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['email','username','phonenumber','invest']
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
