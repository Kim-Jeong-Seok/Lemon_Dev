from django.db import models
from django.conf import settings
from accounts.models import user
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

# 공지사항
class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45, null=False, verbose_name='제목')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='내용')
    date = models.DateTimeField(default=timezone.now, verbose_name='날짜')
    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'notice' 
