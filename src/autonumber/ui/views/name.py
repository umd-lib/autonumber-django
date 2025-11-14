from typing import Any

from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
  CreateView,
  DeleteView,
  DetailView,
  ListView,
  UpdateView,
)

from autonumber.ui.forms import NameForm
from autonumber.ui.models import Name


class NameListView(ListView):
  model = Name
  context_object_name = 'names'
  paginate_by = 10
  ALLOWED_SORT_FIELDS = ['initials', '-initials']

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Names',
      }
    )
    return context

  def get_queryset(self):
    queryset = super().get_queryset()
    query = self.request.GET.get('q')

    if query:
      queryset = queryset.filter(initials__icontains=query)

    sort_by = self.request.GET.get('sort')

    if sort_by in self.ALLOWED_SORT_FIELDS:
      queryset = queryset.order_by(sort_by)
    else:
      queryset = queryset.order_by('initials')

    return queryset


class NameDetailView(DetailView):
  model = Name
  context_object_name = 'name'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Name',
      }
    )
    return context


class NameCreateView(CreateView):
  model = Name
  form_class = NameForm

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Create Name',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Name was successfully created.')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'There was a problem creating the name.')
    return super().form_invalid(form)


class NameUpdateView(UpdateView):
  model = Name
  form_class = NameForm

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Update Name',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Name was successfully updated.')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'There was a problem updating the name.')
    return super().form_invalid(form)


class NameDeleteView(DeleteView):
  model = Name
  success_url = reverse_lazy('name_list')

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Delete Name',
      }
    )
    return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    try:
      self.object.delete()
      messages.success(self.request, 'Name was successfully destroyed.')
      return redirect(self.success_url)
    except ProtectedError:
      messages.error(self.request, 'Name cannot be removed because it has associated Auto Numbers.')
      return redirect(self.object.get_absolute_url())
