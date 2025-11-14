from typing import Any

from django.views.generic import (
  DetailView,
  ListView,
)

from autonumber.ui.models import User


class UserListView(ListView):
  model = User
  context_object_name = 'users'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update({
        'title': 'Users',
    })
    return context


class UserDetailView(DetailView):
  model = User
  context_object_name = 'user'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context.update({
        'title': 'User',
    })
    return context
