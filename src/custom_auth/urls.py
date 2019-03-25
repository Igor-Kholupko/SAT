from django.urls import path, include

from custom_auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
]
