from django.db import models
from django.conf import settings
from accounts.models import user
from django.utils import timezone
# Create your models here.

class Qna(models.Model):
    qna_id = models.AutoField(primary_key=True)
    status = models.BooleanField(null=False)
    qna_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=45, null=False)
    content = models.TextField(null=False)
    file = models.CharField(max_length=255, blank=True, null=True)
    reply = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=False)
    
    
    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'qna'