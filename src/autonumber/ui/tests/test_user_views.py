import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_should_get_index(authorized_client):
    url = reverse('user_list')
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert 'users' in response.context

@pytest.mark.django_db
def test_should_show_user(authorized_client, user_one):
    url = reverse('user_detail', kwargs={'pk': user_one.pk})
    response = authorized_client.get(url)

    assert response.status_code == 200
