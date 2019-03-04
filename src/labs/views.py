from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from labs.models import Task
from labs.forms import TaskForm


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/create.html'
    success_url = reverse_lazy('task_create')


class TaskDetail(DetailView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/detail.html'
