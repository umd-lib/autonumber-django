import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from autonumber.ui.models import Name


@pytest.mark.django_db
def test_should_get_index(authorized_client):
  url = reverse('name_list')
  response = authorized_client.get(url)

  assert response.status_code == 200
  assert 'names' in response.context


@pytest.mark.django_db
def test_should_get_new(authorized_client):
  url = reverse('name_create')
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_create_name(authorized_client):
  count_before = Name.objects.count()

  form_data = {'initials': 'new-initials'}

  url = reverse('name_create')
  response = authorized_client.post(url, data=form_data)

  assert Name.objects.count() == count_before + 1

  new_name = Name.objects.last()
  assert response.status_code == 302
  expected_url = reverse('name_detail', kwargs={'pk': new_name.pk})
  assert response.url == expected_url


@pytest.mark.django_db
def test_should_show_name(authorized_client, name_one):
  url = reverse('name_detail', kwargs={'pk': name_one.pk})
  response = authorized_client.get(url)

  assert response.status_code == 200
  # Add this back when your UI is built:
  # assert str(name_one.initials) in str(response.content)


@pytest.mark.django_db
def test_should_get_edit(authorized_client, name_one):
  url = reverse('name_update', kwargs={'pk': name_one.pk})
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_update_name(authorized_client, name_one):
  update_data = {'initials': 'updated-initials'}

  url = reverse('name_update', kwargs={'pk': name_one.pk})
  response = authorized_client.post(url, data=update_data)

  assert response.status_code == 302
  expected_url = reverse('name_detail', kwargs={'pk': name_one.pk})
  assert response.url == expected_url

  name_one.refresh_from_db()
  assert name_one.initials == 'updated-initials'


@pytest.mark.django_db
def test_should_not_destroy_name_with_auto_numbers(authorized_client, name_one, auto_number_one):
  count_before = Name.objects.count()

  url = reverse('name_delete', kwargs={'pk': name_one.pk})
  response = authorized_client.post(url)

  assert Name.objects.count() == count_before

  assert response.status_code == 302
  assert response.url == reverse('name_detail', kwargs={'pk': name_one.pk})


@pytest.mark.django_db
def test_should_destroy_name_without_auto_numbers(authorized_client):
  # New name without dependencies
  new_name = Name.objects.create(initials='ini')
  count_before = Name.objects.count()

  url = reverse('name_delete', kwargs={'pk': new_name.pk})
  response = authorized_client.post(url)

  assert Name.objects.count() == count_before - 1
  assert response.status_code == 302

  expected_url = reverse('name_list')
  assert response.url == expected_url


@pytest.mark.django_db
def test_name_list_pagination(authorized_client, names):
  url = reverse('name_list')
  response = authorized_client.get(url)

  assert response.status_code == 200
  assertTemplateUsed(response, 'ui/name_list.html')

  assert response.context['is_paginated'] is True
  assert len(response.context['object_list']) == 10

  assertContains(response, names[0].get_absolute_url())
  assertContains(response, names[9].get_absolute_url())

  assertNotContains(response, names[10].get_absolute_url())


@pytest.mark.django_db
def test_name_list_sorting(authorized_client):
  # Create two specific objects to test sorting
  old_obj = Name.objects.create(initials='one')
  new_obj = Name.objects.create(initials='two')

  url = reverse('name_list')

  response_asc = authorized_client.get(url, {'sort': 'initials'})
  assert response_asc.context['object_list'][0] == old_obj

  response_desc = authorized_client.get(url, {'sort': '-initials'})
  assert response_desc.context['object_list'][0] == new_obj
