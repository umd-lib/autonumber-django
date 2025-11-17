from datetime import date
from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from autonumber.ui.forms import AutoNumberForm
from autonumber.ui.models import AutoNumber, Name, Repository


class AutoNumberListView(ListView):
  model = AutoNumber
  context_object_name = 'auto_numbers'
  paginate_by = 10
  ALLOWED_SORT_FIELDS = [
    'id',
    '-id',
    'entry_date',
    '-entry_date',
    'name__initials',
    '-name__initials',
    'repository__name',
    '-repository__name',
  ]

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Auto Numbers',
      }
    )
    return context

  def get_queryset(self):
    queryset = super().get_queryset()
    query = self.request.GET.get('q')

    if query:
      queryset = queryset.filter(Q(name__initials__icontains=query) | Q(repository__name__icontains=query)).distinct()

    sort_by = self.request.GET.get('sort')

    if sort_by in self.ALLOWED_SORT_FIELDS:
      queryset = queryset.order_by(sort_by)
    else:
      queryset = queryset.order_by('-id')

    return queryset


class AutoNumberDetailView(DetailView):
  model = AutoNumber
  context_object_name = 'auto_number'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Auto Number',
      }
    )
    return context


class AutoNumberCreateView(CreateView):
  model = AutoNumber
  form_class = AutoNumberForm

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Create Auto Number',
      }
    )
    return context

  def get_initial(self):
    # Equivalent to building nested objects in Rails
    return {'name': Name(), 'repository': Repository(), 'entry_date': date.today()}

  def form_valid(self, form):
    # mimic Rails’ auto_number_params logic
    data = form.cleaned_data
    repo_name = data.get('repository_name', '').lower().strip()
    name_initials = data.get('name_initials', '').lower().strip()

    repository, _ = Repository.objects.get_or_create(name=repo_name)
    name, _ = Name.objects.get_or_create(initials=name_initials)

    auto_number = form.save(commit=False)
    auto_number.repository = repository
    auto_number.name = name
    auto_number.save()

    messages.success(self.request, f'Created new number: {auto_number.id}')
    return redirect(auto_number.get_absolute_url())

  def form_invalid(self, form):
    for field, error_list in form.errors.items():
      for error in error_list:
        if field == '__all__':
          messages.error(self.request, error)
        else:
          field_label = form.fields[field].label
          messages.error(self.request, f'{field_label}: {error}')

    return super().form_invalid(form)


class AutoNumberUpdateView(UpdateView):
  model = AutoNumber
  form_class = AutoNumberForm

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Update Auto Number',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Autonumber was successfully updated.')
    return super().form_valid(form)

  def form_invalid(self, form):
    for field, error_list in form.errors.items():
      for error in error_list:
        if field == '__all__':
          messages.error(self.request, error)
        else:
          field_label = form.fields[field].label
          messages.error(self.request, f'{field_label}: {error}')

    return super().form_invalid(form)


class AutoNumberDeleteView(DeleteView, SuccessMessageMixin):
  model = AutoNumber
  success_url = reverse_lazy('autonumber_list')

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Delete Auto Number',
      }
    )
    return context

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()
    messages.success(self.request, 'Autonumber was successfully destroyed.')
    return redirect(self.success_url)
