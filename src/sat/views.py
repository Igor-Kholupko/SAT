from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

from sat.exceptions import BadRequest, PermissionDenied


class AjaxableResponseMixin:
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
