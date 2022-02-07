from django.contrib import admin
from .models import Notice

# 공지사항
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
    ) 
