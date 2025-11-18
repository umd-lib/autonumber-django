from django.shortcuts import redirect, render


def login(request):
  if request.user.is_authenticated:
    return redirect('batch')
  else:
    return render(request, 'ui/login.html')
