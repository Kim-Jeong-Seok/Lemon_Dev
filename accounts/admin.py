from django.contrib import admin
from accounts.models import user, Notice

# Register your models here.

@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
        'email',
        'phonenumber',
    )
    

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
    )