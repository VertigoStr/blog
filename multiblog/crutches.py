from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect


class AnonRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is not authenticated.
    """
    redirect_field_name = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)