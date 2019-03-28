from django.urls import path

from labs import views

app_name = 'labs'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
