from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect


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
