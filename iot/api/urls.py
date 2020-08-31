from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers, viewsets
from .views import api_login, get_emails

app_name = "iot"

urlpatterns = [
    path('login', api_login, name='api_login'),
    path('get_emails', get_emails, name='emails')
]

