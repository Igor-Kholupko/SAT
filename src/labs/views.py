from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from labs.models import Task, Discipline, Group
from labs.forms import TaskForm, DisciplineForm, GroupForm


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/create.html'
    success_url = reverse_lazy('task_create')


class TaskDetail(DetailView):
    model = Task
    form_class = TaskForm
    template_name = 'labs/task/detail.html'


class DisciplineCreate(CreateView):
    model = Discipline
    form_class = DisciplineForm
    template_name = 'labs/discipline/create.html'
    success_url = reverse_lazy('discipline_create')


class DisciplineDetail(DetailView):
    model = Discipline
    form_class = DisciplineForm
    template_name = 'labs/discipline/detail.html'


class GroupCreate(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'labs/group/create.html'
    success_url = reverse_lazy('group_create')


class GroupDetail(DetailView):
    model = Group
    form_class = GroupForm
    template_name = 'labs/group/detail.html'