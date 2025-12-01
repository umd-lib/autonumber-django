import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from autonumber.ui.models import AutoNumber, CollectingArea


@pytest.mark.django_db
def test_must_have_name():
  collecting_area = CollectingArea()

  with pytest.raises(ValidationError):
    collecting_area.full_clean()


@pytest.mark.django_db
def test_valid_collecting_area_can_save():
  collecting_area = CollectingArea(name='repo')

  collecting_area.full_clean()
  collecting_area.save()
  collecting_area.refresh_from_db()

  assert collecting_area.name == 'repo'


@pytest.mark.django_db
def test_collecting_area_without_auto_numbers_can_be_deleted():
  collecting_area = CollectingArea.objects.create(name='repo')
  repo_id = collecting_area.id

  collecting_area.delete()

  with pytest.raises(CollectingArea.DoesNotExist):
    CollectingArea.objects.get(id=repo_id)


@pytest.mark.django_db
def test_collecting_area_with_auto_numbers_cannot_be_deleted(name_one, collecting_area_one):
  # The fixtures come from conftest.py
  AutoNumber.objects.create(name=name_one, collecting_area=collecting_area_one)

  with pytest.raises(ProtectedError):
    collecting_area_one.delete()
