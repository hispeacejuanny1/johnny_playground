#accounts/urls.py

from django.urls import path
from .views import CustomLoginView, signup

urlpatterns = [
    path('signup/', signup, name='signup'), #views.signup
    path('login/', CustomLoginView.as_view(), name='login'),
]
