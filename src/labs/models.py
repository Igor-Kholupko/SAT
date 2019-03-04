from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import MinLengthValidator


def one_day_hence():
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    return tomorrow.date()


def _teacher_directory_path(instance, filename):
    return 'teacher_{0}/{1}'.format(instance.user.id, filename)


class Task(models.Model):
    description = models.TextField(_('description'), null=True, blank=True)
    variant = models.PositiveSmallIntegerField(_('variant'), null=True, blank=True)
    deadline = models.DateField(_('deadline'), default=one_day_hence())
    attachment = models.FileField(_('attachment'), upload_to=_teacher_directory_path, null=True, blank=True)

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')


class Discipline(models.Model):
    name = models.CharField(_('discipline name'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('discipline')
        verbose_name_plural = _('disciplines')


class Group(models.Model):
    number = models.CharField(_('group number'), max_length=6, validators=[MinLengthValidator(6)], unique=True)

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
