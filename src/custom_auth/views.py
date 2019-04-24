import re

from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views.generic import View, DetailView

from custom_auth.models import User, Teacher
from custom_auth.forms import UserPersonalInfoForm, StudentPersonalInfoForm, TeacherPersonalInfoForm


def _teacher_url_parser(url):
    if re.match(r'^[a-z]+(-[a-z]+)?-[a-z]-[a-z]$', url):
        full_name = [word.capitalize() for word in re.split(r'-', url)]
        username = full_name[0] if len(full_name) == 3 else full_name[0] + '-' + full_name[1]
        return username + full_name[-2][0] + full_name[-1][0]
    return None


class AjaxableLoginResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'redirect': self.get_success_url(),
            }
            return JsonResponse(data)
        else:
            return response


class LoginView(AjaxableLoginResponseMixin, _LoginView):
    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url=reverse_lazy('labs:dashboard')))
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def redirect_from_start_page(request):
    if request.user.is_anonymous:
        return redirect('login')
    return redirect('labs:dashboard')


class UserPersonalInfoView(View):
    model = User
    context_object_name = 'person'
    template_name = 'custom_auth/personal_page/personal_page_view.html'

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous, login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid')

        qs = self.model.objects.filter(id=uid)
        if qs.exists():
            return render(request, self.template_name, {self.context_object_name: qs.first()})
        else:
            return JsonResponse("Bad Request", status=400)


UserPersonalInfoView.view = UserPersonalInfoView.as_view()


class PersonalInfoDetail(DetailView):
    model = User
    form_class = UserPersonalInfoForm
    template_name = 'custom_auth/personal_page/personal_page_detail.html'
    success_url = '/dashboard/'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous, login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk') == request.user.id:
            self.object = self.model.objects.get(pk=kwargs.get('pk'))
            context = self.get_context_data(**kwargs)
            context['personal_info'] = UserPersonalInfoForm(initial={
                'first_name': self.object.first_name,
                'surname': self.object.surname,
                'patronymic': self.object.patronymic,
                'email': self.object.email,
                'phone_number': self.object.phone_number
            })

            if request.user.is_student:
                context['student_info'] = StudentPersonalInfoForm(initial={
                    'faculty': request.user.student.faculty,
                    'speciality': request.user.student.speciality,
                    'year_of_studying': request.user.student.year_of_studying,
                    'group': request.user.student.group,
                })
            if request.user.is_teacher:
                context['teacher_info'] = TeacherPersonalInfoForm(initial={
                    'academic_position': request.user.teacher.academic_position,
                    'administrative_position': request.user.teacher.administrative_position,
                    'academic_degree': request.user.teacher.academic_degree,
                    'auditorium': request.user.teacher.auditorium,
                })
            return self.render_to_response(context)

        return HttpResponseRedirect(reverse_lazy('labs:dashboard'))

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk') == request.user.id:
            user_form = UserPersonalInfoForm(self.request.POST)
            student_form = StudentPersonalInfoForm(self.request.POST) if request.user.is_student else None
            teacher_form = TeacherPersonalInfoForm(self.request.POST) if request.user.is_teacher else None

            if user_form.is_valid():
                if student_form and teacher_form is None:
                    if student_form.is_valid():
                        self.form_valid(user_form)
                elif student_form is None and teacher_form:
                    if teacher_form.is_valid():
                        self.form_valid(user_form, teacher_form)
                elif student_form and teacher_form:
                    if student_form.is_valid() and teacher_form.is_valid():
                        self.form_valid(user_form, teacher_form)
            else:
                return self.form_invalid(user_form, student_form, teacher_form)

        return HttpResponseRedirect(reverse_lazy('labs:dashboard'))

    def form_valid(self, user_form, teacher_form=None):
        User.objects.filter(
            first_name=user_form.instance.first_name,
            surname=user_form.instance.surname,
            patronymic=user_form.instance.patronymic
        ).update(phone_number=user_form.instance.phone_number,
                 email=user_form.instance.email)

        if teacher_form:
            Teacher.objects.filter(
                user__first_name=user_form.instance.first_name,
                user__surname=user_form.instance.surname,
                user__patronymic=user_form.instance.patronymic
            ).update(academic_position=teacher_form.instance.academic_position,
                     administrative_position=teacher_form.instance.administrative_position,
                     academic_degree=teacher_form.instance.academic_degree,
                     auditorium=teacher_form.instance.auditorium)

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, user_form, student_form=None, teacher_form=None):
        context = self.get_context_data()
        context['personal_info'] = user_form
        context['student_info'] = student_form
        context['teacher_info'] = teacher_form
        return self.render_to_response(context)
