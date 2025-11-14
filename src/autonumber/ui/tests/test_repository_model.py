import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from autonumber.ui.models import AutoNumber, Repository


@pytest.mark.django_db
def test_must_have_name():
  repository = Repository()

  with pytest.raises(ValidationError):
    repository.full_clean()


@pytest.mark.django_db
def test_valid_repository_can_save():
  repository = Repository(name='repo')

  repository.full_clean()
  repository.save()
  repository.refresh_from_db()

  assert repository.name == 'repo'


@pytest.mark.django_db
def test_repository_without_auto_numbers_can_be_deleted():
  repository = Repository.objects.create(name='repo')
  repo_id = repository.id

  repository.delete()

  with pytest.raises(Repository.DoesNotExist):
    Repository.objects.get(id=repo_id)


@pytest.mark.django_db
def test_repository_with_auto_numbers_cannot_be_deleted(name_one, repository_one):
  # The fixtures come from conftest.py
  AutoNumber.objects.create(name=name_one, repository=repository_one)

  with pytest.raises(ProtectedError):
    repository_one.delete()
