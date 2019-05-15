from django.contrib import admin

from labs.models import (
    Discipline, Group, StudyClass, Task, Lesson, Attendance, Mark, TaskVariant
)


class VariantInlineAdmin(admin.TabularInline):
    model = TaskVariant
    exclude = ()
    extra = 0


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
    inlines = [VariantInlineAdmin]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Lesson._meta.local_concrete_fields]
    exclude = ()


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Attendance._meta.local_concrete_fields]
    exclude = ()


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Mark._meta.local_concrete_fields]
    exclude = ()
