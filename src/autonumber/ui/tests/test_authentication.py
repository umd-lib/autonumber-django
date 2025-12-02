import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_autonumber_views_require_login(client, auto_number_one):
  protected_url = reverse('autonumber_list')
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('autonumber_create')
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('autonumber_detail', kwargs={'pk': auto_number_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('autonumber_update', kwargs={'pk': auto_number_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('autonumber_delete', kwargs={'pk': auto_number_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url


@pytest.mark.django_db
def test_collecting_area_views_require_login(client, collecting_area_one):
  protected_url = reverse('collecting_area_list')
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('collecting_area_create')
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('collecting_area_detail', kwargs={'pk': collecting_area_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('collecting_area_update', kwargs={'pk': collecting_area_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('collecting_area_delete', kwargs={'pk': collecting_area_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url


@pytest.mark.django_db
def test_user_views_require_login(client, user_one):
  protected_url = reverse('user_list')
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url

  protected_url = reverse('user_detail', kwargs={'pk': user_one.pk})
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url


@pytest.mark.django_db
def test_batch_view_requires_login(client):
  protected_url = reverse('batch')
  response = client.get(protected_url)

  assert response.status_code == 302

  expected_redirect_url = f'/?next={protected_url}'
  assert response.url == expected_redirect_url
