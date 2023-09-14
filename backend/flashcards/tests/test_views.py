import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from flashcards.models import FlashcardStack, Flashcard, Priority
from conftest import CommonData


@pytest.mark.django_db
class TestFlashcardStack(CommonData):
    def test_unauthorized_cant_make_flashcard_stack(self):
        response = APIClient().post(path='/api/flashcards/flashcardstacks/listcreate/', data=self.create_public_flashcard_stack_data, format='json')
        assert response.status_code == 401

    def test_authorized_client_can_make_flashcard_stack(self, authenticated_client):
        response = authenticated_client.post(path='/api/flashcards/flashcardstacks/listcreate/', data=self.create_public_flashcard_stack_data, format='json')
        assert response.status_code == 201

    def test_unauthorized_can_get_public_flashcard_stack_list(self, create_public_flashcard_stack):
        response = APIClient().get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_unauthorizsed_cant_get_private_flashcard_stack_list(self, create_private_flashcard_stack):
        response = APIClient().get(path='/api/flashcards/flashcardstacks/listcreate/', format='json')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_author_can_access_their_own_stack(self, create_private_flashcard_stack, authenticated_client):
        response = authenticated_client.get(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 200

    def test_author_cant_access_other_users_private_stack(self, create_private_flashcard_stack2, authenticated_client):
        response = authenticated_client.get(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack2.id}/', format='json')
        assert response.status_code == 403

