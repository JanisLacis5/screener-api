from django.urls import path, include
from . import views

urlpatterns = [
    path('stock-screener/', views.say_hi)
]