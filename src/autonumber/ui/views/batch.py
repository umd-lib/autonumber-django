from typing import Any

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from autonumber.ui.forms import BatchForm
from autonumber.ui.models import AutoNumber, Name, Repository


class BatchView(View):
  template_name = 'batch/new.html'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update({
        'title': 'Create Multiple Autonumbers',
    })
    return context

  def get(self, request):
    """Render the new batch form"""
    form = BatchForm()
    return render(request, self.template_name, {'form': form})

  def post(self, request):
    """Handle batch creation"""
    form = BatchForm(request.POST)

    if form.is_valid():
      cleaned = form.cleaned_data
      quantity = cleaned['quantity']

      repository, _ = Repository.objects.get_or_create(name=cleaned['repository_name'])
      name, _ = Name.objects.get_or_create(initials=cleaned['name_initials'])

      auto_number_params = {
        'entry_date': cleaned['entry_date'],
        'repository': repository,
        'name': name,
      }

      stats = AutoNumber.create_batch(quantity, auto_number_params)

      for key, val in stats.items():
        messages.success(request, f'{key}: {val}')

      return redirect('batch')

    # --- Invalid form ---
    # The form object *already* has all the errors.
    # Just re-render the template. Your template (e.g., {{ form.errors }})
    # will automatically show "Quantity must be >= 1", "This field is required", etc.
    return render(request, self.template_name, {'form': form})
