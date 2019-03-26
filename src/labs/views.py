from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

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
        kwargs['has_file_field'] = True
        kwargs['redirect_field_name'] = REDIRECT_FIELD_NAME
        kwargs['datalist'] = list(Task.objects.all())
        return super().get_context_data(**kwargs)


class TaskDetail(DetailView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['datalist'] = list(Task.objects.all())
        return super().get_context_data(**kwargs)


def site_base(request):
    return render(request, 'site_base.html', context={

    })


def sign_in(request):
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user:
            login(request, user)
            return redirect('/admin')
    return render(request, 'signin/sign_in.html', context={
    })


def dashboard(request):
    return render(request, 'labs/dashboard/dashboard.html', context={

    })


def issue(request):
    return render(request, 'teacherworkspace/issue.html', context={

    })
