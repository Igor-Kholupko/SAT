from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from labs.models import Task
from labs.forms import TaskForm


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/create.html'
    success_url = reverse_lazy('task_create')

    def get_success_url(self):
        success_url = self.request.POST.get(REDIRECT_FIELD_NAME, None)
        return success_url or super().get_success_url()

    def get_context_data(self, **kwargs):
        kwargs['redirect_field_name'] = REDIRECT_FIELD_NAME
        return super().get_context_data(**kwargs)


class TaskDetail(DetailView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/detail.html'
