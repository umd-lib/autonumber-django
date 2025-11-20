from django.shortcuts import redirect, render

from autonumber.ui.models import User


def login(request):
  authenticated = request.user.is_authenticated
  included = User.objects.filter(cas_directory_id=request.user.username).exists()

  if authenticated and included:
    return redirect('batch')
  else:
    return render(request, 'ui/login.html', {'authenticated': authenticated})
