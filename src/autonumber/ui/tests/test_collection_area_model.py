import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from autonumber.ui.models import AutoNumber, CollectionArea


@pytest.mark.django_db
def test_must_have_name():
  collection_area = CollectionArea()

  with pytest.raises(ValidationError):
    collection_area.full_clean()


@pytest.mark.django_db
def test_valid_collection_area_can_save():
  collection_area = CollectionArea(name='repo')

  collection_area.full_clean()
  collection_area.save()
  collection_area.refresh_from_db()

  assert collection_area.name == 'repo'


@pytest.mark.django_db
def test_collection_area_without_auto_numbers_can_be_deleted():
  collection_area = CollectionArea.objects.create(name='repo')
  repo_id = collection_area.id

  collection_area.delete()

  with pytest.raises(CollectionArea.DoesNotExist):
    CollectionArea.objects.get(id=repo_id)


@pytest.mark.django_db
def test_collection_area_with_auto_numbers_cannot_be_deleted(name_one, collection_area_one):
  # The fixtures come from conftest.py
  AutoNumber.objects.create(name=name_one, collection_area=collection_area_one)

  with pytest.raises(ProtectedError):
    collection_area_one.delete()
