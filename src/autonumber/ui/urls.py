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
from autonumber.ui.views.batch import BatchView
from autonumber.ui.views.collection_area import (
  CollectionAreaCreateView,
  CollectionAreaDeleteView,
  CollectionAreaDetailView,
  CollectionAreaListView,
  CollectionAreaUpdateView,
)
from autonumber.ui.views.user import (
  UserDetailView,
  UserListView,
)

urlpatterns = [
  path('', login, name='root'),
  path('batch/', BatchView.as_view(), name='batch'),
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
  path('collection_areas/', CollectionAreaListView.as_view(), name='collection_area_list'),
  path('collection_areas/new/', CollectionAreaCreateView.as_view(), name='collection_area_create'),
  path(
    'collection_areas/<int:pk>/',
    CollectionAreaDetailView.as_view(),
    name='collection_area_detail',
  ),
  path(
    'collection_areas/<int:pk>/edit/',
    CollectionAreaUpdateView.as_view(),
    name='collection_area_update',
  ),
  path(
    'collection_areas/<int:pk>/delete/',
    CollectionAreaDeleteView.as_view(),
    name='collection_area_delete',
  ),
]


def get_navigation_links(request: HttpRequest):
  authenticated = request.user.is_authenticated
  included = User.objects.filter(cas_directory_id=request.user.username).exists()

  if authenticated and included:
    return {
      'autonumber_list': 'Autonumbers',
      'collection_area_list': 'Collection Areas',
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
