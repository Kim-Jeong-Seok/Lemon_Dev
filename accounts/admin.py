from django.contrib import admin
from accounts.models import user
from django.forms import TextInput, Textarea
from django.db import models


@admin.register(user)
class UserAdmin(admin.ModelAdmin):

    list_display = [
        'uid',
        'username',
        'email',
        'phonenumber',
        'invest',
        'invest_date',
        'pin',
    ]
    list_editable = [
        'username',
        'email',
        'phonenumber',
        'invest',
        'invest_date',
        'pin',
    ]
    search_fields = ['uid', 'username']
    list_per_page = 20