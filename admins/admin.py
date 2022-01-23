from django.contrib import admin
from .models import Qna

@admin.register(Qna)
class QnaAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'qna_date',
        'user',
        'status',
    ]
    list_filter = ['status', 'category']
    search_fields = ['title']
    fieldsets = [
        ('문의내용', {'fields': ['qna_date', 'category', 'title', 'content', 'file']}),
        ('답변내용', {'fields': ['reply', 'status']}),
    ]