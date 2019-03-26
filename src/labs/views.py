from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from labs.models import Task
from labs.forms import TaskForm


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/create.html'
    success_url = reverse_lazy('task_create')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        success_url = self.request.POST.get(REDIRECT_FIELD_NAME, None)
        return success_url or super().get_success_url()

    def get_context_data(self, **kwargs):
        kwargs['has_file_field'] = True
        kwargs['redirect_field_name'] = REDIRECT_FIELD_NAME
        kwargs['datalist'] = list(Task.objects.all())
        return super().get_context_data(**kwargs)


class TaskDetail(DetailView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['datalist'] = list(Task.objects.all())
        return super().get_context_data(**kwargs)


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'labs/dashboard/dashboard.html', context={

    })

