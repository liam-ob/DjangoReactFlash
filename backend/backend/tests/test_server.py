import pytest

from rest_framework.test import APIClient

from conftest import CommonData


@pytest.mark.django_db
class TestThrottling(CommonData):
    def test_client_can_make_100_requests_per_hour(self, create_user):
        client = APIClient()
        # Query a public flashcard stack 100 times
        for _ in range(100):
            response = client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
            assert response.status_code == 200
        response = client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
        assert response.status_code == 429

    def test_authenticated_client_can_make_1000_requests_per_hour(self, authenticated_client):
        for _ in range(1000):
            response = authenticated_client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
            assert response.status_code == 200
        response = authenticated_client.get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
        assert response.status_code == 429
