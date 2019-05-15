from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from custom_auth.models import User, Group as CustomGroup, Student, Teacher

admin.site.unregister(Group)

admin.site.register(CustomGroup)


class StudentInlineAdmin(admin.TabularInline):
    model = Student
    exclude = ()


class TeacherInlineAdmin(admin.TabularInline):
    model = Teacher
    exclude = ()


@admin.register(User)
class UserAdmin(_UserAdmin):
    """
    Class for admin generic views of User model.
    Includes default admin options.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'surname', 'patronymic', 'email')}),
        (_('Permissions'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'surname', 'patronymic', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email')
    list_filter = ('groups',)
    search_fields = ('username', 'email')
    ordering = ('-id',)
    filter_horizontal = ('groups',)
    inlines = [StudentInlineAdmin, TeacherInlineAdmin]
