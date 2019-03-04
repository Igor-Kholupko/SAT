from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView

from labs.models import Task
from labs.forms import TaskForm


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = ''  # insert necessary
    success_url = reverse_lazy('')  # insert necessary

