import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from autonumber.ui.models import CollectingArea


@pytest.mark.django_db
def test_should_get_index(authorized_client):
  url = reverse('collecting_area_list')
  response = authorized_client.get(url)

  assert response.status_code == 200
  assert 'collecting_areas' in response.context


@pytest.mark.django_db
def test_should_get_new(authorized_client):
  url = reverse('collecting_area_create')
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_create_collecting_area(authorized_client):
  count_before = CollectingArea.objects.count()

  form_data = {'name': 'MY-NEW-REPO'}

  url = reverse('collecting_area_create')
  response = authorized_client.post(url, data=form_data)

  assert CollectingArea.objects.count() == count_before + 1

  new_repo = CollectingArea.objects.last()
  assert new_repo.name == 'my-new-repo'

  assert response.status_code == 302
  expected_url = reverse('collecting_area_detail', kwargs={'pk': new_repo.pk})
  assert response.url == expected_url


@pytest.mark.django_db
def test_should_show_collecting_area(authorized_client, collecting_area_one):
  url = reverse('collecting_area_detail', kwargs={'pk': collecting_area_one.pk})
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_get_edit(authorized_client, collecting_area_one):
  url = reverse('collecting_area_update', kwargs={'pk': collecting_area_one.pk})
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_update_collecting_area(authorized_client, collecting_area_one):
  update_data = {'name': 'UPDATED-NAME'}

  url = reverse('collecting_area_update', kwargs={'pk': collecting_area_one.pk})
  response = authorized_client.post(url, data=update_data)

  assert response.status_code == 302
  expected_url = reverse('collecting_area_detail', kwargs={'pk': collecting_area_one.pk})
  assert response.url == expected_url

  collecting_area_one.refresh_from_db()
  assert collecting_area_one.name == 'updated-name'


@pytest.mark.django_db
def test_should_not_destroy_collecting_area_with_auto_numbers(authorized_client, collecting_area_one, auto_number_one):
  count_before = CollectingArea.objects.count()

  url = reverse('collecting_area_delete', kwargs={'pk': collecting_area_one.pk})
  response = authorized_client.post(url)

  assert CollectingArea.objects.count() == count_before

  assert response.status_code == 302
  assert response.url == reverse('collecting_area_detail', kwargs={'pk': collecting_area_one.pk})


@pytest.mark.django_db
def test_should_destroy_collecting_area_without_auto_numbers(authorized_client):
  # New repo without dependencies
  new_repo = CollectingArea.objects.create(name='deletable-repo')
  count_before = CollectingArea.objects.count()

  url = reverse('collecting_area_delete', kwargs={'pk': new_repo.pk})
  response = authorized_client.post(url)

  assert CollectingArea.objects.count() == count_before - 1
  assert response.status_code == 302

  expected_url = reverse('collecting_area_list')
  assert response.url == expected_url


@pytest.mark.django_db
def test_collecting_area_list_pagination(authorized_client, collecting_areas):
  url = reverse('collecting_area_list')
  response = authorized_client.get(url)

  assert response.status_code == 200
  assertTemplateUsed(response, 'ui/collectingarea_list.html')

  assert response.context['is_paginated'] is True
  assert len(response.context['object_list']) == 10

  assertContains(response, collecting_areas[0].get_absolute_url())
  assertContains(response, collecting_areas[9].get_absolute_url())

  assertNotContains(response, collecting_areas[10].get_absolute_url())


@pytest.mark.django_db
def test_collecting_area_list_sorting(authorized_client):
  # Create two specific objects to test sorting
  old_obj = CollectingArea.objects.create(name='one')
  new_obj = CollectingArea.objects.create(name='two')

  url = reverse('collecting_area_list')

  response_asc = authorized_client.get(url, {'sort': 'name'})
  assert response_asc.context['object_list'][0] == old_obj

  response_desc = authorized_client.get(url, {'sort': '-name'})
  assert response_desc.context['object_list'][0] == new_obj
