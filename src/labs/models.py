from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


def _teacher_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/teacher_<id>/<filename>
    return 'teacher_{0}/{1}'.format(instance.user.id, filename)


class Task(models.Model):
    description = models.TextField(_('description'), null=True, blank=True)
    variant = models.PositiveSmallIntegerField(_('variant'), null=True, blank=True)
    deadline = models.DateField(_('deadline'), default=one_day_hence())
    attachment = models.FileField(_('attachment'), upload_to=_teacher_directory_path, null=True, blank=True)

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
