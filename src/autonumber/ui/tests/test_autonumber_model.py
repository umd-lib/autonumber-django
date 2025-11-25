import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from autonumber.ui.models import AutoNumber

# These tests use three fixtures specified in conftest.py

@pytest.mark.django_db
def test_must_have_name(collection_area_one):
  date = timezone.now().date()

  auto_number = AutoNumber(
    collection_area=collection_area_one,
    entry_date=date,
  )

  with pytest.raises(ValidationError):
    auto_number.full_clean()


@pytest.mark.django_db
def test_must_have_collection_area(name_one):
  date = timezone.now().date()

  auto_number = AutoNumber(
    name=name_one,
    entry_date=date,
  )

  with pytest.raises(ValidationError):
    auto_number.full_clean()


@pytest.mark.django_db
def test_valid_auto_number_can_save(auto_number_one, name_one, collection_area_one):

  # The fixture already created and saved it.
  # Reloading it just to be sure
  auto_number_one.refresh_from_db()

  assert auto_number_one.name == name_one
  assert auto_number_one.collection_area == collection_area_one
  assert str(auto_number_one.entry_date) == '2016-03-31'
