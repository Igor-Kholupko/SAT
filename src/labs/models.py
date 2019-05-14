from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from labs.validators import DateValidator


def task_upload_path(instance, filename):
    return '{0}/{1}'.format(
        slugify(instance.study_class, allow_unicode=True), filename
    )


class Discipline(models.Model):
    name = models.CharField(
        _('discipline name'),
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = _('discipline')
        verbose_name_plural = _('disciplines')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Group(models.Model):
    number = models.CharField(
        _('group number'),
        max_length=6,
        validators=[
            MinLengthValidator(6),
        ],
        unique=True
    )

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        ordering = ('number',)

    def natural_key(self):
        return self.number

    def __str__(self):
        return str(self.number)


from custom_auth.models import Teacher, Student


class StudyClass(models.Model):
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name='study_classes',
        related_query_name='study_class'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='study_classes',
        related_query_name='study_class'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='study_classes',
        related_query_name='study_class'
    )

    class Meta:
        verbose_name = _('study class')
        verbose_name_plural = _('study classes')
        unique_together = (('discipline', 'group'),)
        ordering = ('discipline', 'group',)

    def __str__(self):
        return '{dsc} {grp}'.format(dsc=self.discipline, grp=self.group)


User = get_user_model()


class Task(models.Model):
    title = models.CharField(
        _('title'),
        max_length=100
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True
    )
    variants = models.ManyToManyField(
        User,
        related_name='variants',
        related_query_name='variant',
        through='TaskVariant',
        through_fields=('task', 'assignee')
    )
    deadline = models.DateField(
        _('deadline'),
        validators=[
            DateValidator(),
        ]
    )
    attachment = models.FileField(
        _('attachment'),
        upload_to=task_upload_path,
        null=True,
        blank=True
    )
    study_class = models.ForeignKey(
        StudyClass,
        on_delete=models.CASCADE,
        related_name='tasks',
        related_query_name='task',
        verbose_name=_('study class')
    )
    order = models.PositiveIntegerField(
        _('task number in study class')
    )

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        unique_together = (('study_class', 'order'),)
        ordering = ('study_class', 'order',)

    def __str__(self):
        return '{title}'.format(title=self.title)

    def clean(self):
        data = super().clean()
        return data


class TaskVariant(models.Model):
    task = models.ForeignKey(Task, models.CASCADE)
    assignee = models.ForeignKey(User, models.CASCADE)
    variant = models.TextField(_("Variant"), null=True, blank=True)
    note = models.TextField(_("Note"), null=True, blank=True)


class Lesson(models.Model):
    study_class = models.ForeignKey(
        StudyClass,
        on_delete=models.CASCADE,
        related_name='lessons',
        related_query_name='lesson',
        verbose_name=_('study class')
    )
    date = models.DateField(_('date'))

    class Meta:
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')
        ordering = ('study_class', 'date',)

    def __str__(self):
        return '{date} {sc}'.format(date=self.date, sc=self.study_class)


class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendances',
        related_query_name='attendance',
        verbose_name=_('student')
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='attendances',
        related_query_name='attendance',
        verbose_name=_('lesson')
    )
    attendance = models.BooleanField(
        _('attendance'),
        default=True
    )

    class Meta:
        verbose_name = _('attendance')
        verbose_name_plural = _('attendances')
        ordering = ('lesson', 'student',)

    def __str__(self):
        return '{ls} {std} {atn}'.format(ls=self.lesson, std=self.student, atn=self.attendance)


class Mark(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marks',
        related_query_name='mark',
        verbose_name=_('student')
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='marks',
        related_query_name='mark',
        verbose_name=_('lesson')
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='marks',
        related_query_name='mark',
        verbose_name=_('task')
    )
    mark = models.CharField(
        _('mark'),
        max_length=128,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('mark')
        verbose_name_plural = _('marks')
        unique_together = (('student', 'task'),)
        ordering = ('lesson', 'task', 'student',)

    def __str__(self):
        return '{mrk}'.format(mrk=self.mark)
