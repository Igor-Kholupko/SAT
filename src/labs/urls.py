from django.urls import path

from labs import views

urlpatterns = [
    path('<int:pk>', views.TaskDetail.as_view(), name='task_detail'),
    path('create/', views.TaskCreate.as_view(), name='task_create'),
]
