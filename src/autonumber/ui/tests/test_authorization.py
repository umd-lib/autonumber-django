import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_autonumber_views_not_authorized(authenticated_client, auto_number_one):
  response = authenticated_client.get(reverse('autonumber_list'))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('autonumber_create'))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('autonumber_detail', kwargs={'pk': auto_number_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('autonumber_update', kwargs={'pk': auto_number_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('autonumber_delete', kwargs={'pk': auto_number_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text


@pytest.mark.django_db
def test_repository_views_not_authorized(authenticated_client, repository_one):
  response = authenticated_client.get(reverse('repository_list'))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('repository_create'))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('repository_detail', kwargs={'pk': repository_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('repository_update', kwargs={'pk': repository_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('repository_delete', kwargs={'pk': repository_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text


@pytest.mark.django_db
def test_user_views_not_authorized(authenticated_client, user_one):
  response = authenticated_client.get(reverse('user_list'))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text

  response = authenticated_client.get(reverse('user_detail', kwargs={'pk': user_one.pk}))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text


@pytest.mark.django_db
def test_batch_view_not_authorized(authenticated_client):
  response = authenticated_client.get(reverse('batch'))
  assert response.status_code == 200
  assert 'Not Authorized' in response.text
