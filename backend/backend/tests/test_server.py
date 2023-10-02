import pytest

from rest_framework.test import APIClient
from django.contrib.auth.models import User

from conftest import CommonData

# Create own user so that the authenticated_client doesnt get throttled
@pytest.fixture
def throttle_authenticated_client():
    client = APIClient()
    user_data = {'username': 'throttletestuser', 'password': 'testpassword'}
    user = User.objects.create(**user_data)
    client.post(path='/api/auth/token/login/', data=user_data, format='json')
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestThrottling(CommonData):
    def test_client_can_make_100_requests_per_hour(self, create_user):
        pytest.skip()  # unskipping will make all the request return 429?
        client = APIClient()
        # Query a public flashcard stack 100 times
        for _ in range(100):
            response = client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
            assert response.status_code == 200
        response = client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
        assert response.status_code == 429

    def test_authenticated_client_can_make_1000_requests_per_hour(self, throttle_authenticated_client):
        pytest.skip()  # unskipping will make all the request return 429?
        for _ in range(1000):
            response = throttle_authenticated_client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
            assert response.status_code == 200
        response = throttle_authenticated_client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
        assert response.status_code == 429
