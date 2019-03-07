from django.contrib import admin

from labs.models import (
    Discipline, Group, StudyClass, Task
)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Discipline._meta.local_concrete_fields]
    exclude = ()


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Group._meta.local_concrete_fields]
    exclude = ()


@admin.register(StudyClass)
class StudyClassAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StudyClass._meta.local_concrete_fields]
    exclude = ()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Task._meta.local_concrete_fields]
    exclude = ()
