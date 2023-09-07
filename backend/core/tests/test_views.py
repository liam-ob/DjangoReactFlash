import pytest

from rest_framework.test import APIClient
from django.contrib.auth.models import User


class CommonData:
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPassword',
        'password2': 'TestPassword',
        'name': 'Test User'
    }


@pytest.fixture
def create_user():
    APIClient().post('/api/core/users/', CommonData().user_data, format='json')
    assert User.objects.count() == 1
    return User.objects.get(username=CommonData().user_data['username'])

@pytest.fixture
def user_client(create_user):
    client = APIClient()
    client.login(username=create_user.username, password=create_user.password)
    return client


@pytest.fixture
def authenticated_client(create_user):
    data = CommonData().user_data.copy()
    client = APIClient()
    client.post('/api/core/users/login/', data, format='json')
    return client


@pytest.mark.django_db
class TestUser(CommonData):
    def test_client_can_create_user(self):
        client = APIClient()
        response = client.post(path='/api/core/users/', data=self.user_data, format='json')
        assert response.status_code == 201

    def test_client_cant_create_user_when_submitting_invalid_data(self):
        new_user_data = self.user_data.copy()
        new_user_data['username'] = ''
        response = APIClient().post(path='/api/core/users/', data=new_user_data, format='json')
        assert response.status_code == 400

    def test_client_can_login(self):
        User.objects.create_user(**self.user_data)
        client = APIClient()
        response = client.post(path='/api/core/users/login/', data=self.user_data, format='json')
        assert response.status_code == 200

    def test_user_client_can_get_user_details(self, create_user, user_client):
        response = user_client.get(path=f'/api/core/users/{create_user.id}/', format='json')
        assert response.status_code == 200
        assert response.data['username'] == self.user_data['username']

    def test_client_can_update_user_details(self, create_user, authenticated_client):
        new_user_data = self.user_data.copy()
        new_user_data['username'] = 'newusername'
        response = authenticated_client.put(path=f'/api/core/users/{create_user.id}/', data=new_user_data, format='json')
        assert response.status_code == 200
        assert response.data['username'] == new_user_data['username']

    def test_client_can_delete_user(self, create_user, authenticated_client):
        response = authenticated_client.delete(path=f'/api/core/users/{create_user.id}/', format='json')
        assert response.status_code == 204
        assert User.objects.count() == 0
