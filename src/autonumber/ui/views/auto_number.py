from datetime import date
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from autonumber.ui.forms import AutoNumberForm
from autonumber.ui.mixins import AuthorizationRequiredMixin
from autonumber.ui.models import AutoNumber, CollectionArea, User


class AutoNumberListView(LoginRequiredMixin, AuthorizationRequiredMixin, ListView):
  model = AutoNumber
  context_object_name = 'auto_numbers'
  login_url = "/"
  paginate_by = 10
  ALLOWED_SORT_FIELDS = [
    'id',
    '-id',
    'entry_date',
    '-entry_date',
    'name__initials',
    '-name__initials',
    'collection_area__name',
    '-collection_area__name',
  ]

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Auto Numbers',
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
      queryset = queryset.filter(Q(name__initials__icontains=query) | Q(collection_area__name__icontains=query)).distinct()

    sort_by = self.request.GET.get('sort')

    if sort_by in self.ALLOWED_SORT_FIELDS:
      queryset = queryset.order_by(sort_by)
    else:
      queryset = queryset.order_by('-id')

    return queryset


class AutoNumberDetailView(LoginRequiredMixin, AuthorizationRequiredMixin, DetailView):
  model = AutoNumber
  context_object_name = 'auto_number'
  login_url = "/"

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Auto Number',
      }
    )
    return context


class AutoNumberCreateView(LoginRequiredMixin, AuthorizationRequiredMixin, CreateView):
  model = AutoNumber
  form_class = AutoNumberForm
  login_url = "/"

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update(
      {
        'title': 'Create Auto Number',
      }
    )
    return context

  def get_initial(self):
    return {'collection_area': CollectionArea(), 'entry_date': date.today()}

  def form_valid(self, form):
    self.object = form.save(commit=False)

    cas_directory_id = self.request.user.get_username()
    user = User.objects.filter(cas_directory_id=cas_directory_id).first()
    self.object.name = user.name

    self.object.save()
    messages.success(self.request, f'Created new number: {self.object.id}')

    return redirect(self.object.get_absolute_url())

  def form_invalid(self, form):
    for field, error_list in form.errors.items():
      for error in error_list:
        if field == '__all__':
          messages.error(self.request, error)
        else:
          field_label = form.fields[field].label
          messages.error(self.request, f'{field_label}: {error}')

    return super().form_invalid(form)


class AutoNumberUpdateView(LoginRequiredMixin, AuthorizationRequiredMixin, UpdateView):
  model = AutoNumber
  form_class = AutoNumberForm
  login_url = "/"


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


class AutoNumberDeleteView(LoginRequiredMixin, AuthorizationRequiredMixin, DeleteView, SuccessMessageMixin):
  model = AutoNumber
  success_url = reverse_lazy('autonumber_list')
  login_url = "/"

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
