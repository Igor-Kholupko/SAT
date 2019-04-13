from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.utils.formats import date_format
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from sat.exceptions import BadRequest, PermissionDenied
from labs.models import Discipline
from labs.forms import TaskForm, MarkSetForm, AttendanceSetForm


class UserContextMixin(LoginRequiredMixin, ContextMixin):
    def get_redirect_field_name(self):
        return None

    def handle_no_permission(self):
        redirect = super().handle_no_permission()
        self.request.session[super().get_redirect_field_name()] = self.request.get_full_path()
        return redirect

    def get_context_data(self, **kwargs):
        menu = {}
        if self.request.method == 'GET' and not self.request.is_ajax():
            user = self.request.user
            if user.is_teacher:
                menu.update({_("Teacher sector"): {
                    str(discipline): [
                        (str(study_class.group), urlencode(
                            {'action': 'get_study_class', 'user': 'teacher', 'pk': study_class.pk}
                        )) for study_class in user.teacher.study_classes.filter(discipline__exact=discipline)
                    ] for discipline in Discipline.objects.filter(study_class__teacher__exact=user.teacher).distinct()
                }})
            if user.is_student:
                menu.update({_("Student sector"): {
                    str(user.student.group): [
                        (str(study_class.discipline), urlencode(
                            {'action': 'get_study_class', 'user': 'student', 'pk': study_class.pk}
                        )) for study_class in user.student.group.study_classes.all()
                    ]
                }})
        return super().get_context_data(**kwargs, **{'menu': menu})


class AjaxableDashboardResponseMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            method = getattr(request, request.method, {})
            try:
                if 'action' not in method:
                    raise BadRequest({'reason': _("Request should contain 'action' parameter.")})
                elif not hasattr(self, method['action']):
                    raise BadRequest({'reason': _("Unrecognized action parameter value: '%s'.") % method['action']})
                else:
                    return getattr(self, method['action'])(request, *args, **kwargs)
            except (BadRequest, PermissionDenied) as e:
                return JsonResponse(e.args[0], status=e.http_code)
            except Exception as e:
                return JsonResponse(
                    {'reason': _("Bad parameters."), e.__class__.__name__: e.args}, status=BadRequest.http_code
                )
        return super().dispatch(request, *args, **kwargs)

    def get_study_class(self, request, *args, **kwargs):
        if request.method != 'GET':
            raise BadRequest(
                {'reason': _("%s action must be requested through %s method.") % ('get_study_class', 'GET')}
            )
        if 'user' not in request.GET or 'pk' not in request.GET:
            raise BadRequest({'reason': _("Required parameters missed.")})
        user_type = request.GET['user']
        pk = request.GET['pk']
        if user_type == 'teacher':
            if not request.user.is_teacher:
                raise PermissionDenied({'reason': _("You are not a teacher!")})
            sc = request.user.teacher.study_classes.get(pk=pk)
        elif user_type == 'student':
            if not request.user.is_student:
                raise PermissionDenied({'reason': _("You are not a student!")})
            sc = request.user.student.group.study_classes.get(pk=pk)
        else:
            raise BadRequest({'reason': _("Unrecognized user type: '%s'.") % user_type})
        lessons_list = sc.lessons.all()
        return self.response_class(request, 'workspace.html', context={
            'sc': sc,
            'lessons_list': lessons_list,
            'students_list': [
                (student, {
                    attendance.lesson_id: attendance
                    for attendance in student.attendances.filter(lesson__study_class=sc)
                }, {
                    mark.task_id: mark for mark in student.marks.filter(lesson__study_class=sc)
                }) for student in sc.group.students.all()
            ],
            'task_list': sc.tasks.all(),
            'can_create': request.user.has_perm('labs.add_task'),
            'can_change': request.user.has_perm('labs.change_task'),
            'can_delete': request.user.has_perm('labs.delete_task'),
        })

    def post_mark(self, request, *args, **kwargs):
        if request.method != 'POST':
            raise BadRequest({'reason': _("%s action must be requested through %s method.") % ('post_mark', 'POST')})
        if not request.user.is_teacher:
            raise PermissionDenied({'reason': _("Only teachers can set marks!")})
        form = MarkSetForm(data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'new_mark': str(form.instance),
                'new_date': date_format(form.instance.lesson.date)
            })
        else:
            raise BadRequest(form.errors)

    def post_task(self, request, *args, **kwargs):
        if request.method != 'POST':
            raise BadRequest({'reason': _("%s action must be requested through %s method.") % ('post_task', 'POST')})
        if not request.user.is_teacher:
            raise PermissionDenied({'reason': _("Only teachers can create tasks!")})
        form = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': '',
            })
        else:
            raise BadRequest(form.errors)

    def post_attendance(self, request, *args, **kwargs):
        if request.method != 'POST':
            raise BadRequest(
                {'reason': _("%s action must be requested through %s method.") % ('post_attendance', 'POST')}
            )
        if not request.user.is_teacher:
            raise PermissionDenied({'reason': _("Only teachers can control attendance!")})
        form = AttendanceSetForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('+' if form.instance.attendance else '-')
        else:
            raise BadRequest(form.errors)


class DashboardView(UserContextMixin, AjaxableDashboardResponseMixin, TemplateView):
    template_name = 'labs/dashboard/dashboard.html'
