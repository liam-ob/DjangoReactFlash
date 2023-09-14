import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from conftest import CommonData


@pytest.mark.django_db
class TestUser(CommonData):
    def test_client_can_create_user(self):
        client = APIClient()
        response = client.post(path='/api/core/users/register/', data=self.user_data, format='json')
        assert response.status_code == 201
        assert User.objects.count() == 1

    def test_client_cant_create_user_when_submitting_invalid_data(self):
        new_user_data = self.user_data.copy()
        new_user_data['username'] = ''
        response = APIClient().post(path='/api/core/users/register/', data=new_user_data, format='json')
        assert response.status_code == 400

    def test_client_can_post_random_data_and_it_still_works(self):
        new_user_data = self.user_data.copy()
        new_user_data['random'] = 'random'
        response = APIClient().post(path='/api/core/users/register/', data=new_user_data, format='json')
        assert response.status_code == 201
        assert User.objects.count() == 1

    def test_client_can_login(self, create_user):
        client = APIClient()
        response = client.post(path='/api/core/users/login/', data=self.login_user_data, format='json')
        assert response.status_code == 200

    def test_client_cant_login_with_invalid_credentials(self, create_user):
        new_user_data = {'username': self.user_data['username'], 'password': 'invalid'}
        client = APIClient()
        response = client.post(path='/api/core/users/login/', data=new_user_data, format='json')
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    def test_missing_log_in_field_gives_error(self, create_user):
        new_user_data = {'username': self.user_data['username']}
        client = APIClient()
        response = client.post(path='/api/core/users/login/', data=new_user_data, format='json')
        assert response.status_code == 400
        assert response.data['password'][0] == 'This field is required.'

    def test_token_is_set_successfully_upon_login(self, create_user):
        client = APIClient()
        response = client.post(path='/api/core/users/login/', data=self.login_user_data, format='json')
        assert response.data['token'] is not None

    def test_user_client_cant_get_user_details(self, create_user, user_client):
        response = user_client.get(path=f'/api/core/users/{create_user.id}/', format='json')
        assert response.status_code == 401

    def test_authenticated_client_can_get_user_details(self, create_user, authenticated_client):
        response = authenticated_client.get(path=f'/api/core/users/{create_user.id}/')
        assert response.status_code == 200
        assert response.data['username'] == self.user_data['username']

    def test_client_can_update_user_details(self, create_user, authenticated_client):
        new_user_data = self.user_data.copy()
        new_user_data['username'] = 'newusername'
        response = authenticated_client.put(path=f'/api/core/users/{create_user.id}/', data=new_user_data, format='json')
        assert response.status_code == 200
        assert response.data['username'] == new_user_data['username']

    def test_unauthenticated_cant_update_user_details(self, user_client, create_user):
        new_user_data = self.user_data.copy()
        new_user_data['username'] = 'newusername'
        response = user_client.put(path=f'/api/core/users/{create_user.id}/', data=new_user_data, format='json')
        assert response.status_code == 401

    def test_client_can_delete_user(self, create_user, authenticated_client):
        response = authenticated_client.delete(path=f'/api/core/users/{create_user.id}/', format='json')
        assert response.status_code == 204
        assert User.objects.count() == 0

    def test_unauthenticated_client_cant_delete_user(self, user_client, create_user):
        response = user_client.delete(path=f'/api/core/users/{create_user.id}/', format='json')
        assert response.status_code == 401
        assert User.objects.count() == 1

    def test_one_user_cant_delete_another_user(self, create_user, authenticated_client):
        new_user = User.objects.create_user(
            username='newuser',
            email='user2@user.com',
            password='password',
        )
        response = authenticated_client.delete(path=f'/api/core/users/{new_user.id}/', format='json')
        assert response.status_code == 403
        assert User.objects.count() == 2

    def test_client_can_logout(self, authenticated_client):
        response = authenticated_client.get(path='/api/core/users/logout/', format='json')
        assert response.status_code == 204
        assert Token.objects.count() == 0

    def test_unauthenticated_client_cant_logout(self, user_client):
        response = user_client.post(path='/api/core/users/logout/', format='json')
        assert response.status_code == 401
        assert Token.objects.count() == 0
