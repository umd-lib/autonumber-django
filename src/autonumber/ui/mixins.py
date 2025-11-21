from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render

from autonumber.ui.models import User


class AuthorizationRequiredMixin(AccessMixin):
  """
  Verifies that the authenticated user's CAS Directory ID exists in the User model
  """

  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      # If not logged in, delegate to LoginRequiredMixin's logic
      # (redirects to LOGIN_URL)
      return super().dispatch(request, *args, **kwargs)

    cas_directory_id = request.user.username
    is_authorized = User.objects.filter(cas_directory_id=cas_directory_id).exists()

    if is_authorized:
      return super().dispatch(request, *args, **kwargs)
    else:
      return render(request, 'ui/login.html', {'authenticated': request.user.is_authenticated})

