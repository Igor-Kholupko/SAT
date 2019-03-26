from django.urls import path
from django.contrib.auth.views import LogoutView

from custom_auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
