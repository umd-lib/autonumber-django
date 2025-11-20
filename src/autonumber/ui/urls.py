from django.http import HttpRequest
from django.urls import path

from autonumber.ui.models import User
from autonumber.ui.views import login
from autonumber.ui.views.auto_number import (
  AutoNumberCreateView,
  AutoNumberDeleteView,
  AutoNumberDetailView,
  AutoNumberListView,
  AutoNumberUpdateView,
)
from autonumber.ui.views.autocomplete import autocomplete_names, autocomplete_repositories
from autonumber.ui.views.batch import BatchView
from autonumber.ui.views.name import (
  NameCreateView,
  NameDeleteView,
  NameDetailView,
  NameListView,
  NameUpdateView,
)
from autonumber.ui.views.repository import (
  RepositoryCreateView,
  RepositoryDeleteView,
  RepositoryDetailView,
  RepositoryListView,
  RepositoryUpdateView,
)
from autonumber.ui.views.user import (
  UserDetailView,
  UserListView,
)

urlpatterns = [
  path('', login, name='root'),
  path('batch/', BatchView.as_view(), name='batch'),
  path('autocomplete/names/', autocomplete_names, name='autocomplete_names'),
  path(
    'autocomplete/repositories/',
    autocomplete_repositories,
    name='autocomplete_repositories',
  ),
  path('users/', UserListView.as_view(), name='user_list'),
  path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
  path('auto_numbers/', AutoNumberListView.as_view(), name='autonumber_list'),
  path('auto_numbers/new/', AutoNumberCreateView.as_view(), name='autonumber_create'),
  path(
    'auto_numbers/<int:pk>/',
    AutoNumberDetailView.as_view(),
    name='autonumber_detail',
  ),
  path(
    'auto_numbers/<int:pk>/edit/',
    AutoNumberUpdateView.as_view(),
    name='autonumber_update',
  ),
  path(
    'auto_numbers/<int:pk>/delete/',
    AutoNumberDeleteView.as_view(),
    name='autonumber_delete',
  ),
  path('names/', NameListView.as_view(), name='name_list'),
  path('names/new/', NameCreateView.as_view(), name='name_create'),
  path('names/<int:pk>/', NameDetailView.as_view(), name='name_detail'),
  path('names/<int:pk>/edit/', NameUpdateView.as_view(), name='name_update'),
  path('names/<int:pk>/delete/', NameDeleteView.as_view(), name='name_delete'),
  path('repositories/', RepositoryListView.as_view(), name='repository_list'),
  path('repositories/new/', RepositoryCreateView.as_view(), name='repository_create'),
  path(
    'repositories/<int:pk>/',
    RepositoryDetailView.as_view(),
    name='repository_detail',
  ),
  path(
    'repositories/<int:pk>/edit/',
    RepositoryUpdateView.as_view(),
    name='repository_update',
  ),
  path(
    'repositories/<int:pk>/delete/',
    RepositoryDeleteView.as_view(),
    name='repository_delete',
  ),
]


def get_navigation_links(request: HttpRequest):
  authenticated = request.user.is_authenticated
  included = User.objects.filter(cas_directory_id=request.user.username).exists()

  if authenticated and included:
    return {
      'autonumber_list': 'Autonumbers',
      'name_list': 'Names',
      'repository_list': 'Repos',
      'user_list': 'Users',
      '': f'Logged in as {request.user.username}',
      'cas_ng_logout': 'Log Out',
    }
  elif authenticated:
    return {
      '': f'Logged in as {request.user.username}',
      'cas_ng_logout': 'Log Out',
    }
  else:
    return {'cas_ng_login': 'Log In'}
