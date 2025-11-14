from datetime import date

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from autonumber.ui.models import AutoNumber


@pytest.mark.django_db
def test_should_get_index(client):
  url = reverse('autonumber_list')
  response = client.get(url)

  assert response.status_code == 200
  assert 'auto_numbers' in response.context


@pytest.mark.django_db
def test_should_get_new(client):
  url = reverse('autonumber_create')
  response = client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_create_auto_number(client, name_one, repository_one):
  count_before = AutoNumber.objects.count()

  url = reverse('autonumber_create')
  form_data = {'entry_date': '2025-11-10', 'name': name_one.pk, 'repository': repository_one.pk}
  response = client.post(url, data=form_data)
  assert response.status_code == 302
  assert AutoNumber.objects.count() == count_before + 1

  latest_auto_number = AutoNumber.objects.last()
  expected_url = reverse('autonumber_detail', kwargs={'pk': latest_auto_number.pk})
  assert response.url == expected_url


@pytest.mark.django_db
def test_should_show_auto_number(client, auto_number_one):
  url = reverse('autonumber_detail', kwargs={'pk': auto_number_one.pk})
  response = client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_get_edit(client, auto_number_one):
  url = reverse('autonumber_update', kwargs={'pk': auto_number_one.pk})
  response = client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_update_auto_number(client, auto_number_one, name_two, repository_two):
  update_data = {'entry_date': '2025-11-11', 'name': name_two.pk, 'repository': repository_two.pk}

  url = reverse('autonumber_update', kwargs={'pk': auto_number_one.pk})
  response = client.post(url, data=update_data)
  assert response.status_code == 302

  expected_url = reverse('autonumber_detail', kwargs={'pk': auto_number_one.pk})
  assert response.url == expected_url

  auto_number_one.refresh_from_db()
  assert auto_number_one.name == name_two
  assert auto_number_one.repository == repository_two


@pytest.mark.django_db
def test_should_destroy_auto_number(client, auto_number_one):
  count_before = AutoNumber.objects.count()

  url = reverse('autonumber_delete', kwargs={'pk': auto_number_one.pk})
  response = client.delete(url)
  assert AutoNumber.objects.count() == count_before - 1
  assert response.status_code == 302

  expected_url = reverse('autonumber_list')
  assert response.url == expected_url


@pytest.mark.django_db
def test_autonumber_list_pagination(client, auto_numbers):
  url = reverse('autonumber_list')
  response = client.get(url)

  assert response.status_code == 200
  assertTemplateUsed(response, 'ui/autonumber_list.html')

  assert response.context['is_paginated'] is True
  assert len(response.context['object_list']) == 10

  assertContains(response, auto_numbers[14].get_absolute_url())
  assertContains(response, auto_numbers[5].get_absolute_url())

  assertNotContains(response, auto_numbers[4].get_absolute_url())


@pytest.mark.django_db
def test_autonumber_list_sorting(client, name_one, repository_one):
  # Create two specific objects to test sorting
  old_obj = AutoNumber.objects.create(entry_date=date(2020, 1, 1), name=name_one, repository=repository_one)
  new_obj = AutoNumber.objects.create(entry_date=date(2026, 1, 1), name=name_one, repository=repository_one)

  url = reverse('autonumber_list')

  response_asc = client.get(url, {'sort': 'entry_date'})
  assert response_asc.context['object_list'][0] == old_obj

  response_desc = client.get(url, {'sort': '-entry_date'})
  assert response_desc.context['object_list'][0] == new_obj


@pytest.mark.django_db
def test_index_should_include_web_accessibility_link(client):
  url = reverse('autonumber_list')
  response = client.get(url)

  assert response.status_code == 200
  assertContains(response, 'href="https://umd.edu/web-accessibility"')
