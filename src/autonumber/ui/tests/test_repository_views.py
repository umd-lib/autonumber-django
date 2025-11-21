import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from autonumber.ui.models import Repository


@pytest.mark.django_db
def test_should_get_index(authorized_client):
  url = reverse('repository_list')
  response = authorized_client.get(url)

  assert response.status_code == 200
  assert 'repositories' in response.context


@pytest.mark.django_db
def test_should_get_new(authorized_client):
  url = reverse('repository_create')
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_create_repository(authorized_client):
  count_before = Repository.objects.count()

  form_data = {'name': 'MY-NEW-REPO'}

  url = reverse('repository_create')
  response = authorized_client.post(url, data=form_data)

  assert Repository.objects.count() == count_before + 1

  new_repo = Repository.objects.last()
  assert new_repo.name == 'my-new-repo'

  assert response.status_code == 302
  expected_url = reverse('repository_detail', kwargs={'pk': new_repo.pk})
  assert response.url == expected_url


@pytest.mark.django_db
def test_should_show_repository(authorized_client, repository_one):
  url = reverse('repository_detail', kwargs={'pk': repository_one.pk})
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_get_edit(authorized_client, repository_one):
  url = reverse('repository_update', kwargs={'pk': repository_one.pk})
  response = authorized_client.get(url)

  assert response.status_code == 200


@pytest.mark.django_db
def test_should_update_repository(authorized_client, repository_one):
  update_data = {'name': 'UPDATED-NAME'}

  url = reverse('repository_update', kwargs={'pk': repository_one.pk})
  response = authorized_client.post(url, data=update_data)

  assert response.status_code == 302
  expected_url = reverse('repository_detail', kwargs={'pk': repository_one.pk})
  assert response.url == expected_url

  repository_one.refresh_from_db()
  assert repository_one.name == 'updated-name'


@pytest.mark.django_db
def test_should_not_destroy_repository_with_auto_numbers(authorized_client, repository_one, auto_number_one):
  count_before = Repository.objects.count()

  url = reverse('repository_delete', kwargs={'pk': repository_one.pk})
  response = authorized_client.post(url)

  assert Repository.objects.count() == count_before

  assert response.status_code == 302
  assert response.url == reverse('repository_detail', kwargs={'pk': repository_one.pk})


@pytest.mark.django_db
def test_should_destroy_repository_without_auto_numbers(authorized_client):
  # New repo without dependencies
  new_repo = Repository.objects.create(name='deletable-repo')
  count_before = Repository.objects.count()

  url = reverse('repository_delete', kwargs={'pk': new_repo.pk})
  response = authorized_client.post(url)

  assert Repository.objects.count() == count_before - 1
  assert response.status_code == 302

  expected_url = reverse('repository_list')
  assert response.url == expected_url


@pytest.mark.django_db
def test_repository_list_pagination(authorized_client, repositories):
  url = reverse('repository_list')
  response = authorized_client.get(url)

  assert response.status_code == 200
  assertTemplateUsed(response, 'ui/repository_list.html')

  assert response.context['is_paginated'] is True
  assert len(response.context['object_list']) == 10

  assertContains(response, repositories[0].get_absolute_url())
  assertContains(response, repositories[9].get_absolute_url())

  assertNotContains(response, repositories[10].get_absolute_url())


@pytest.mark.django_db
def test_repository_list_sorting(authorized_client):
  # Create two specific objects to test sorting
  old_obj = Repository.objects.create(name='one')
  new_obj = Repository.objects.create(name='two')

  url = reverse('repository_list')

  response_asc = authorized_client.get(url, {'sort': 'name'})
  assert response_asc.context['object_list'][0] == old_obj

  response_desc = authorized_client.get(url, {'sort': '-name'})
  assert response_desc.context['object_list'][0] == new_obj
