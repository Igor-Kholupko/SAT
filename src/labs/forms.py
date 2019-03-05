from django import forms
from labs.models import Task, Discipline, Group


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description', 'variant', 'deadline', 'attachment')


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ('name',)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('number',)
