from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('number_bingo/', views.number_bingo, name='number_bingo'),
]