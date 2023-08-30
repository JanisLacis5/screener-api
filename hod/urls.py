from django.urls import path, include
from . import views

urlpatterns = [
    path('hod/', views.say_hi)
]