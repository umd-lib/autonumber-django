import pytest

from autonumber.ui.models import AutoNumber, CollectingArea, User


@pytest.fixture
def name_one():
  return 'Name One'


@pytest.fixture
def collecting_area_one():
  return CollectingArea.objects.create(name='Repo One')


@pytest.fixture
def collecting_area_two():
  return CollectingArea.objects.create(name='repo-two')


@pytest.fixture
def user_one():
  return User.objects.create(cas_directory_id='user-one', name='Test User')


@pytest.fixture
def auto_number_one(name_one, collecting_area_one):
  """
  Pytest will automatically run name_one and collecting_area_one
  and pass their results into this fixture.
  """
  return AutoNumber.objects.create(
    entry_date='2016-03-31',
    name=name_one,
    collecting_area=collecting_area_one,
  )


@pytest.fixture
def auto_numbers(name_one, collecting_area_one):
  """
  Provides 15 AutoNumber objects to force pagination.
  """
  auto_nums = []
  for i in range(15):
    auto_nums.append(AutoNumber.objects.create(entry_date='2025-01-01', name=name_one, collecting_area=collecting_area_one))
  return auto_nums


@pytest.fixture
def collecting_areas():
  """
  Provides 15 Name objects, created out of alphabetical order
  to properly test sorting.
  """
  created_collecting_areas = []
  # Create 15 collecting areas from 'A' to 'O'
  for char_code in range(ord('A'), ord('P')):
    created_collecting_areas.append(CollectingArea.objects.create(name=chr(char_code)))

  return created_collecting_areas


@pytest.fixture
def authenticated_client(client, django_user_model):
  """
  Logs an arbitrary user into the Django test client
  They will not be authorized
  Used within tests for verifying authentication and autorization
  """
  user = django_user_model.objects.create_user(username='not_in_user_table', password='foobar')
  client.force_login(user)
  return client


@pytest.fixture
def authorized_client(client, django_user_model, user_one):
  """
  Logs user_one into the Django test client
  With user_one added in the User Model they will be also authorized
  Used within test checking the functionality of each view
  """
  user = django_user_model.objects.create_user(username=user_one.cas_directory_id, password='foobar')
  client.force_login(user)
  return client
