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

from autonumber.ui.forms import RepositoryForm
from autonumber.ui.models import Repository


class RepositoryListView(LoginRequiredMixin, ListView):
  model = Repository
  context_object_name = 'repositories'
  login_url = '/'
  paginate_by = 10
  ALLOWED_SORT_FIELDS = ['name', '-name']

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Repositories',
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


class RepositoryDetailView(LoginRequiredMixin, DetailView):
  model = Repository
  context_object_name = 'repository'
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Repository',
      }
    )
    return context


class RepositoryCreateView(LoginRequiredMixin, CreateView):
  model = Repository
  form_class = RepositoryForm
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Create Repository',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Repository was successfully created.')
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


class RepositoryUpdateView(LoginRequiredMixin, UpdateView):
  model = Repository
  form_class = RepositoryForm
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Update Repository',
      }
    )
    return context

  def form_valid(self, form):
    messages.success(self.request, 'Repository was successfully updated.')
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


class RepositoryDeleteView(LoginRequiredMixin, DeleteView):
  model = Repository
  success_url = reverse_lazy('repository_list')
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Delete Repository',
      }
    )
    return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()

    try:
      self.object.delete()
      messages.success(request, 'Repository was successfully destroyed.')
      return redirect(self.success_url)
    except ProtectedError:
      messages.error(request, 'Repository cannot be removed because it has associated Auto Numbers.')
      return redirect(self.object.get_absolute_url())
