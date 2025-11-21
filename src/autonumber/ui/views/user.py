from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
  DetailView,
  ListView,
)

from autonumber.ui.mixins import AuthorizationRequiredMixin
from autonumber.ui.models import User


class UserListView(LoginRequiredMixin, AuthorizationRequiredMixin, ListView):
  model = User
  context_object_name = 'users'
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update({
        'title': 'Users',
    })
    return context


class UserDetailView(LoginRequiredMixin, AuthorizationRequiredMixin, DetailView):
  model = User
  context_object_name = 'user'
  login_url = '/'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update({
        'title': 'User',
    })
    return context
