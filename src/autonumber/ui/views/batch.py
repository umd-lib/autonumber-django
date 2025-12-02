from datetime import date
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from autonumber.ui.forms import BatchForm
from autonumber.ui.mixins import AuthorizationRequiredMixin
from autonumber.ui.models import AutoNumber, User


class BatchView(LoginRequiredMixin, AuthorizationRequiredMixin, View):
  template_name = 'batch/new.html'
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Create Multiple Autonumbers',
      }
    )
    return context

  def get(self, request):
    cas_directory_id = self.request.user.get_username()
    user = User.objects.filter(cas_directory_id=cas_directory_id).first()
    initial_data = {'entry_date': date.today(), 'quantity': 1, 'name': user.name}

    form = BatchForm(initial=initial_data)
    return render(request, self.template_name, {'form': form})

  def post(self, request):
    form = BatchForm(request.POST)

    if form.is_valid():
      cleaned = form.cleaned_data
      quantity = cleaned['quantity']

      collecting_area = cleaned['collecting_area']
      cas_directory_id = self.request.user.get_username()
      user = User.objects.filter(cas_directory_id=cas_directory_id).first()

      auto_number_params = {
        'entry_date': cleaned['entry_date'],
        'collecting_area': collecting_area,
        'name': user.name,
      }

      stats = AutoNumber.create_batch(quantity, auto_number_params)
      quantity = stats['count']
      first = stats['first']
      last = stats['last']

      messages.success(self.request, f'Created {quantity} Autonumbers ({first}-{last})')

      return redirect('batch')

    # --- Invalid form ---
    # The form object *already* has all the errors.
    # Just re-render the template. Your template (e.g., {{ form.errors }})
    # will automatically show "Quantity must be >= 1", "This field is required", etc.
    return render(request, self.template_name, {'form': form})
