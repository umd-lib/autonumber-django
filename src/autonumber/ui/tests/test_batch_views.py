import pytest
from django.urls import reverse

from autonumber.ui.models import AutoNumber


@pytest.mark.django_db
def test_should_get_new(client):
  url = reverse('batch')
  response = client.get(url)

  assert response.status_code == 200
  # A FormView will put 'form' in the context
  assert 'form' in response.context


@pytest.mark.django_db
def test_should_create_auto_number_batch(client, auto_number_one):
  quantity_to_add = 10
  count_before = AutoNumber.objects.count()

  form_data = {
    'entry_date': auto_number_one.entry_date,
    'name': auto_number_one.name.initials,
    'repository': auto_number_one.repository.pk,
    'quantity': quantity_to_add,
  }

  url = reverse('batch')
  response = client.post(url, data=form_data)

  assert AutoNumber.objects.count() == count_before + quantity_to_add

  assert response.status_code == 302
  expected_url = reverse('batch')
  assert response.url == expected_url


@pytest.mark.django_db
def test_require_name(client, auto_number_one):
  count_before = AutoNumber.objects.count()

  form_data = {
    'entry_date': auto_number_one.entry_date,
    'repository_name': auto_number_one.repository.pk,
    'quantity': 10,
  }

  url = reverse('batch')
  response = client.post(url, data=form_data)

  assert AutoNumber.objects.count() == count_before

  assert response.status_code == 200
  assert 'form' in response.context
  assert 'name' in response.context['form'].errors


@pytest.mark.django_db
def test_require_repository(client, auto_number_one):
  count_before = AutoNumber.objects.count()

  form_data = {'entry_date': auto_number_one.entry_date, 'name_initials': auto_number_one.name.initials, 'quantity': 10}

  url = reverse('batch')
  response = client.post(url, data=form_data)

  assert AutoNumber.objects.count() == count_before
  assert response.status_code == 200
  assert 'form' in response.context
  assert 'repository' in response.context['form'].errors


@pytest.mark.django_db
def test_require_non_nil_quantity(client, auto_number_one):
  count_before = AutoNumber.objects.count()

  form_data = {
    'entry_date': auto_number_one.entry_date,
    'name': auto_number_one.name.initials,
    'repository': auto_number_one.repository.pk,
    # 'quantity' is omitted
  }

  url = reverse('batch')
  response = client.post(url, data=form_data)

  assert AutoNumber.objects.count() == count_before
  assert response.status_code == 200
  assert 'form' in response.context
  assert 'quantity' in response.context['form'].errors


@pytest.mark.django_db
def test_require_non_negative_quantity(client, auto_number_one):
  count_before = AutoNumber.objects.count()

  form_data = {
    'entry_date': auto_number_one.entry_date,
    'name': auto_number_one.name.initials,
    'repository': auto_number_one.repository.pk,
    'quantity': -10
  }

  url = reverse('batch')
  response = client.post(url, data=form_data)

  assert response.status_code == 200
  assert AutoNumber.objects.count() == count_before

  assert 'form' in response.context
  assert 'quantity' in response.context['form'].errors
  assert 'Ensure this value is greater than or equal to 1' in str(response.context['form'].errors['quantity'])
