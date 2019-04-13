from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url


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
                'redirect': response.url,
            }
            return JsonResponse(data)
        else:
            return response


class LoginView(AjaxableLoginResponseMixin, _LoginView):
    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url=reverse_lazy('labs:dashboard'),
                                       redirect_field_name=None))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.session.get(
            self.redirect_field_name,
            self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, '')
            )
        )
        self.request.session.pop(self.redirect_field_name, ())
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''
