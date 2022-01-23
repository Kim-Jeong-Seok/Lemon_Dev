from django.urls import path, include
from . import views

app_name='admins'
urlpatterns = [
    path('qna', views.qna),
]