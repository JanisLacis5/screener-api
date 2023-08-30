from django.urls import path, include
from . import views

urlpatterns = [
    path('hod/', views.send_hod_data)
]
