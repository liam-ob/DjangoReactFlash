import pytest

from rest_framework.test import APIClient

@pytest.fixture
class UserFixtures:
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPassword',
    }

    def create_user(self):
        APIClient().post('/api/users/', self.user_data, format='json')

    def authenticated_client(self):
        client = APIClient()
        client.login(username=self.user_data['username'], password=self.user_data['password'])
        return client