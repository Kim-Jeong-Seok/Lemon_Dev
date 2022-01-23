from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import user

# Create your views here.
def qna(request):
    
    return render(request, 'qna.html')