from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.postgres.fields import JSONField
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

    def __str__(self):
        return str(self.number)


class StudyClass(models.Model):
    discipline = models.ForeignKey(
        Discipline,
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
    variant = JSONField(
        _('variant'),
        null=True,
        blank=True
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
        return '{title} ({sc})'.format(title=self.title, sc=self.study_class)

    def clean(self):
        data = super().clean()
        return data
