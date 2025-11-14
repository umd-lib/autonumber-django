import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_should_get_index(client):
    url = reverse('user_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'users' in response.context

@pytest.mark.django_db
def test_should_show_user(client, user_one):
    url = reverse('user_detail', kwargs={'pk': user_one.pk})
    response = client.get(url)

    assert response.status_code == 200
    # You can add this back when your UI is built:
    # assert str(user_one.name) in str(response.content)
