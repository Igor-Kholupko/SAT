from django.urls import path, include

from labs import views

task_patterns = [
    path('<int:pk>', views.TaskDetail.as_view(), name='task_detail'),
    path('create/', views.TaskCreate.as_view(), name='task_create'),
]

discipline_patterns = [
    path('<int:pk>', views.DisciplineDetail.as_view(), name='discipline_detail'),
    path('create/', views.DisciplineCreate.as_view(), name='discipline_create'),
]

urlpatterns = [
    path('task/', include(task_patterns)),
    path('discipline/', include(discipline_patterns)),
]
