import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from autonumber.ui.models import AutoNumber, Name


@pytest.mark.django_db
def test_must_have_initials():
  name = Name()

  with pytest.raises(ValidationError):
    name.full_clean()


@pytest.mark.django_db
def test_valid_name_can_save():
  name = Name(initials='pme')

  name.full_clean()
  name.save()
  name.refresh_from_db()

  assert name.initials == 'pme'


@pytest.mark.django_db
def test_name_without_auto_numbers_can_be_deleted():
  name = Name.objects.create(initials='pme')
  name_id = name.id

  name.delete()

  with pytest.raises(Name.DoesNotExist):
    Name.objects.get(id=name_id)


@pytest.mark.django_db
def test_name_with_auto_numbers_cannot_be_deleted(name_one, repository_one):
  # The fixtures come from conftest.py
  AutoNumber.objects.create(name=name_one, repository=repository_one)

  with pytest.raises(ProtectedError):
    name_one.delete()
