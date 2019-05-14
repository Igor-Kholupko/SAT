from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from labs.models import Task, Mark, Attendance, TaskVariant


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'study_class')

    def save(self, commit=True):
        from django.utils.timezone import now
        self.instance.deadline = now().date()
        self.instance.order = self.instance.study_class.tasks.all().count() + 1
        return super().save(commit)


class MarkSetForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('mark', 'student', 'task')

    def __init__(self, data, *args, **kwargs):
        qs = self._meta.model.objects.filter(student=data.get('student'), task=data.get('task'))
        kwargs['instance'] = qs.first() if qs.exists else None
        self.lesson = None
        super().__init__(data, *args, **kwargs)

    def clean(self):
        cd = super().clean()
        current_day = now().date()
        lqs = cd['task'].study_class.lessons.filter(date__lte=current_day)
        if not lqs.exists():
            raise ValidationError(_("Can't find nearest lesson."))
        self.lesson = lqs.first()

    def save(self, commit=True):
        self.instance.lesson = self.lesson
        return super().save(commit)


class AttendanceSetForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'


class TaskVariantForm(forms.ModelForm):
    class Meta:
        model = TaskVariant
        fields = '__all__'


TaskVariantFormSet = inlineformset_factory(
    Task, TaskVariant, form=TaskVariantForm,fields=['assignee', 'variant', 'note'], extra=3, can_delete=False
)
