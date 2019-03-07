from django.urls import path, include

from labs import views


task_patterns = ([
    path('<int:pk>', views.TaskDetail.as_view(), name='details'),
    path('create/', views.TaskCreate.as_view(), name='create'),
], 'task')

app_name = 'labs'

urlpatterns = [
    path('task/', include(task_patterns)),
]
