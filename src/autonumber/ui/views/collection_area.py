from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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

from autonumber.ui.forms import CollectionAreaForm
from autonumber.ui.mixins import AuthorizationRequiredMixin
from autonumber.ui.models import CollectionArea


class CollectionAreaListView(LoginRequiredMixin, AuthorizationRequiredMixin, ListView):
  model = CollectionArea
  context_object_name = 'collection_areas'
  login_url = '/'
  paginate_by = 10
  ALLOWED_SORT_FIELDS = ['name', '-name']

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Collection Areas',
      }
    )

    paginator = context['paginator']
    page_obj = context['page_obj']

    if paginator:
      context.update(
        {
          'elided_page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1),
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
      queryset = queryset.order_by('name')

    return queryset


class CollectionAreaDetailView(LoginRequiredMixin, AuthorizationRequiredMixin, DetailView):
  model = CollectionArea
  context_object_name = 'collection_area'
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Collection Area',
      }
    )
    return context


class CollectionAreaCreateView(LoginRequiredMixin, AuthorizationRequiredMixin, CreateView):
  model = CollectionArea
  form_class = CollectionAreaForm
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Create Collection Area',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Collection Area was successfully created.')
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


class CollectionAreaUpdateView(LoginRequiredMixin, AuthorizationRequiredMixin, UpdateView):
  model = CollectionArea
  form_class = CollectionAreaForm
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Update Collection Area',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Collection Area was successfully updated.')
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


class CollectionAreaDeleteView(LoginRequiredMixin, AuthorizationRequiredMixin, DeleteView):
  model = CollectionArea
  success_url = reverse_lazy('collection_area_list')
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Delete Collection Area',
      }
    )
    return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()

    try:
      self.object.delete()
      messages.success(request, 'Collection Area was successfully destroyed.')
      return redirect(self.success_url)
    except ProtectedError:
      messages.error(request, 'Collection Area cannot be removed because it has associated Auto Numbers.')
      return redirect(self.object.get_absolute_url())
