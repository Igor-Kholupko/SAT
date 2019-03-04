from django import forms
from labs.models import Task, Discipline


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description', 'variant', 'deadline', 'attachment')


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ('name',)
