import pytest
from django.core.exceptions import ValidationError

from autonumber.ui.models import User


@pytest.mark.django_db
def test_must_have_name_and_directory_id():
  user = User()

  with pytest.raises(ValidationError):
    user.full_clean()


@pytest.mark.django_db
def test_must_have_name():
  user = User(cas_directory_id='rollotomasi')

  with pytest.raises(ValidationError):
    user.full_clean()


@pytest.mark.django_db
def test_must_have_directory_id():
  user = User(name='Rollo Tomasi')

  with pytest.raises(ValidationError):
    user.full_clean()


@pytest.mark.django_db
def test_valid_user():
  user = User(cas_directory_id='rollotomasi', name='Rollo Tomasi')

  user.full_clean()
