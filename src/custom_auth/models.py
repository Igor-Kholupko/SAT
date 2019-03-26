import sys
import re

from django.db import models
from django.contrib.auth.models import (
    Group as _Group, AbstractUser, UserManager,
    send_mail
)
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

from labs.models import Group as StudyGroup

from custom_auth.consts import FACULTIES


class Group(_Group):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def save(self, *args, **kwargs):
        if len(sys.argv) > 1 and sys.argv[1] in ['migrate', 'loaddata']:
            return super(Group, self).save(*args, **kwargs)
        else:
            raise PermissionError(_("This model objects can not be save."))

    def delete(self, *args, **kwargs):
        if len(sys.argv) > 1 and sys.argv[1] in ['migrate']:
            return super(Group, self).save(*args, **kwargs)
        else:
            raise PermissionError(_("This model objects can not be save."))


class User(AbstractUser):
    username_validator = RegexValidator(regex=r'^(([A-Z][a-z]+(-[A-Z][a-z]+)?[A-Z]{2})|\d{7})$')
    name_validator = RegexValidator(regex=r'[A-ZА-ЯЁ][a-zа-яё]+(-[A-ZА-ЯЁ][a-zа-яё]+)?')
    phone_validator = RegexValidator(regex=r'^\+?375(17|25|29|33|44)\d{7}$')

    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Student card number of a student or surname and initials of a teacher.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        _('first name'),
        max_length=15,
        help_text=_('First name of a student or of a teacher.'),
        validators=[name_validator]
    )
    surname = models.CharField(
        _('surname'),
        max_length=25,
        help_text=_('Surname of a student or of a teacher.'),
        validators=[name_validator]
    )
    patronymic = models.CharField(
        _('patronymic'),
        max_length=20,
        help_text=_('Patronymic name of a student or of a teacher.'),
        validators=[name_validator]
    )
    email = models.EmailField(
        _('email address'),
        blank=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(default=True)
    phone_number = models.CharField(
        _('phone number'),
        max_length=13,
        validators=[phone_validator],
        blank=True,
        null=True
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'surname', 'patronymic', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('username',)
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student',
        verbose_name=_('user')
    )
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name='students',
        related_query_name='student',
        verbose_name=_('study group')
    )
    faculty = models.PositiveSmallIntegerField(
        _('faculty'),
        choices=FACULTIES
    )
    year_of_studying = models.PositiveSmallIntegerField(
        _('year of study'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    speciality = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')
        ordering = ('group',)

    def get_faculty_abbreviation(self):
        return ''.join(word[0] for word in re.split(r'\W+', self.get_faculty_display()))

    def promotion_rates(self):
        self.year_of_studying = self.year_of_studying + 1


class Teacher(models.Model):
    auditorium_validator = RegexValidator(regex=r'^\d{3}[a-z]?-[1-9]$')

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='teacher',
        verbose_name=_('user')
    )
    academic_position = models.CharField(
        _('academic position'),
        max_length=100,
        null=True,
        blank=True
    )
    administrative_position = models.CharField(
        _('administrative position'),
        max_length=100,
        null=True,
        blank=True
    )
    academic_degree = models.CharField(
        _('academic degree'),
        max_length=50,
        null=True,
        blank=True
    )
    auditorium = models.CharField(
        _('auditorium'),
        max_length=5,
        help_text=_("Required. Format: auditorium-campus."),
        validators=[auditorium_validator]
    )

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

