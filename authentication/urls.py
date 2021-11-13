from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path('obtain_token/', views.obtain_token),
    path('validate_token/', views.validate_token),
]
