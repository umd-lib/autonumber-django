import pytest

from autonumber.ui.models import AutoNumber, Name, Repository, User


@pytest.fixture
def name_one():
  return Name.objects.create(initials='Name One')


@pytest.fixture
def repository_one():
  return Repository.objects.create(name='Repo One')


@pytest.fixture
def auto_number_one(name_one, repository_one):
  """
  Pytest will automatically run name_one and repository_one
  and pass their results into this fixture.
  """
  return AutoNumber.objects.create(
    entry_date='2016-03-31',
    name=name_one,
    repository=repository_one,
  )


@pytest.fixture
def user_one():
  return User.objects.create(cas_directory_id='user-one', name='Test User')


@pytest.fixture
def name_two():
  return Name.objects.create(initials='name-two')


@pytest.fixture
def repository_two():
  return Repository.objects.create(name='repo-two')


@pytest.fixture
def auto_numbers(name_one, repository_one):
  """
  Provides 15 AutoNumber objects to force pagination.
  """
  auto_nums = []
  for i in range(15):
    auto_nums.append(AutoNumber.objects.create(entry_date='2025-01-01', name=name_one, repository=repository_one))
  return auto_nums


@pytest.fixture
def names():
  """
  Provides 15 Name objects, created out of alphabetical order
  to properly test sorting.
  """
  created_names = []
  # Create 15 names from 'A' to 'O'
  for char_code in range(ord('A'), ord('P')):
    created_names.append(Name.objects.create(initials=chr(char_code)))

  return created_names

@pytest.fixture
def repositories():
  """
  Provides 15 Name objects, created out of alphabetical order
  to properly test sorting.
  """
  created_repositories = []
  # Create 15 repositories from 'A' to 'O'
  for char_code in range(ord('A'), ord('P')):
    created_repositories.append(Repository.objects.create(name=chr(char_code)))

  return created_repositories
