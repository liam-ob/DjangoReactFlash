import pytest
from django.db import IntegrityError

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from flashcards.models import FlashcardStack, Flashcard, Priority
from conftest import CommonData


@pytest.mark.django_db
class TestFlashcardStack(CommonData):
    # CREATE
    def test_unauthorized_cant_make_flashcard_stack(self):
        response = APIClient().post(path='/api/flashcards/flashcardstacks/listcreate/', data=self.create_public_flashcard_stack_data, format='json')
        assert response.status_code == 401

    def test_authorized_client_can_make_flashcard_stack(self, authenticated_client):
        response = authenticated_client.post(path='/api/flashcards/flashcardstacks/listcreate/', data=self.create_public_flashcard_stack_data, format='json')
        assert response.status_code == 201

    # READ
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

    def test_unauthorized_cant_access_private_stack(self, create_private_flashcard_stack):
        response = APIClient().get(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 403

    # UPDATE
    def test_author_can_update_their_own_stack(self, create_private_flashcard_stack, authenticated_client):
        new_data = self.create_private_flashcard_stack_data.copy()
        new_data['name'] = 'brobeans'
        response = authenticated_client.put(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', data=new_data, format='json')
        assert response.status_code == 200
        assert response.data['name'] == 'brobeans'

    def test_authenticated_user_cant_update_someone_elses_stack(self, create_private_flashcard_stack, authenticated_client2):
        new_data = self.create_private_flashcard_stack_data.copy()
        new_data['name'] = 'brobeans'
        response = authenticated_client2.put(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', data=new_data, format='json')
        assert response.status_code == 403

    def test_unauthorized_cant_update_stack(self, create_private_flashcard_stack):
        new_data = self.create_private_flashcard_stack_data.copy()
        new_data['name'] = 'brobeans'
        response = APIClient().put(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', data=new_data, format='json')
        assert response.status_code == 401

    def test_updated_flashcard_stack_gets_updated_date_modified(self, create_private_flashcard_stack, authenticated_client):
        new_data = self.create_private_flashcard_stack_data.copy()
        new_data['name'] = 'brobeans'
        response = authenticated_client.put(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', data=new_data, format='json')
        assert response.status_code == 200
        assert response.data['date_modified'] != create_private_flashcard_stack.date_modified

    # DELETE
    def test_author_can_delete_their_own_stack(self, create_private_flashcard_stack, authenticated_client):
        response = authenticated_client.delete(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 204
        assert FlashcardStack.objects.count() == 0

    def test_authenticated_user_cant_delete_someone_elses_stack(self, create_private_flashcard_stack, authenticated_client2):
        response = authenticated_client2.delete(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 403
        assert FlashcardStack.objects.count() == 1

    def test_unauthorized_cant_delete_stack(self, create_private_flashcard_stack):
        response = APIClient().delete(path=f'/api/flashcards/flashcardstacks/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 401
        assert FlashcardStack.objects.count() == 1


@pytest.mark.django_db
class TestFlashcards(CommonData):
    # CREATE
    def test_auhtenticated_can_make_a_private_flashcard(self, create_private_flashcard_stack, authenticated_client):
        flashcard_data = self.create_flashcard_data.copy()
        flashcard_data['stack_id'] = create_private_flashcard_stack.id
        response = authenticated_client.post(path=f'/api/flashcards/flashcards/listcreate/{create_private_flashcard_stack.id}/', data=flashcard_data, format='json')
        assert response.status_code == 201
        assert Flashcard.objects.count() == 1

    def test_authenticated_client_can_make_a_public_flashcard(self, create_public_flashcard_stack, authenticated_client):
        flashcard_data = self.create_flashcard_data.copy()
        flashcard_data['stack_id'] = create_public_flashcard_stack.id
        response = authenticated_client.post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=flashcard_data, format='json')
        assert response.status_code == 201
        assert Flashcard.objects.count() == 1

    def test_authenticated_client_cant_make_a_flashcard_without_a_stack(self, authenticated_client, create_public_flashcard_stack):
        response = authenticated_client.post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=self.create_flashcard_data, format='json')
        assert response.status_code == 400
        assert response.data['stack_id'] == 'This field is required.'

    def test_unauthenticated_cant_make_a_flashcard(self, create_public_flashcard_stack):
        response = APIClient().post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=self.create_flashcard_data, format='json')
        assert response.status_code == 401
        assert Flashcard.objects.count() == 0

    def test_authenticated_client_cant_make_a_flashcard_for_another_stack(self, create_public_flashcard_stack, authenticated_client2):
        flashcard_data = self.create_flashcard_data.copy()
        flashcard_data['stack_id'] = create_public_flashcard_stack.id
        response = authenticated_client2.post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=flashcard_data, format='json')
        assert response.status_code == 403
        assert Flashcard.objects.count() == 0

    def test_authenticated_client_cant_make_a_flashcard_without_an_answer(self, create_public_flashcard_stack, authenticated_client):
        flashcard_data = self.create_flashcard_data.copy()
        flashcard_data['stack_id'] = create_public_flashcard_stack.id
        flashcard_data.pop('answer_char')
        response = authenticated_client.post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=flashcard_data, format='json')
        assert response.status_code == 400
        assert response.data['answer_char'] == 'This field is required.'

    def test_authenticated_client_cant_make_a_flashcard_without_a_question(self, create_public_flashcard_stack, authenticated_client):
        flashcard_data = self.create_flashcard_data.copy()
        flashcard_data['stack_id'] = create_public_flashcard_stack.id
        flashcard_data.pop('question')
        response = authenticated_client.post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=flashcard_data, format='json')
        assert response.status_code == 400
        assert response.data['question'][0] == 'This field is required.'

    def test_authenticated_client_can_make_a_flashcard_with_both_answer_types(self, create_public_flashcard_stack, authenticated_client, create_image):
        flashcard_data = self.create_flashcard_data.copy()
        flashcard_data['stack_id'] = create_public_flashcard_stack.id
        flashcard_data['answer_img'] = create_image
        response = authenticated_client.post(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', data=flashcard_data, format='multipart')
        assert response.status_code == 201
        assert Flashcard.objects.count() == 1

    # READ
    def test_unauthenticated_can_get_public_flashcard(self, create_public_flashcard, create_public_flashcard_stack):
        response = APIClient().get(path=f'/api/flashcards/flashcards/listcreate/{create_public_flashcard_stack.id}/', format='json')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_author_can_get_private_flashcard_list(self, create_private_flashcard, authenticated_client, create_private_flashcard_stack):
        response = authenticated_client.get(path=f'/api/flashcards/flashcards/listcreate/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_author_can_get_their_own_private_flashcard(self, create_private_flashcard, authenticated_client):
        response = authenticated_client.get(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', format='json')
        assert response.status_code == 200

    def test_unauthenticated_cant_access_private_flashcard(self, create_private_flashcard, create_private_flashcard_stack):
        response = APIClient().get(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', format='json')
        assert response.status_code == 403

    def test_authenticated_can_access_other_authors_private_flashcard(self, create_private_flashcard_stack, create_private_flashcard, authenticated_client2):
        response = authenticated_client2.get(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', format='json')
        assert response.status_code == 403

    # UPDATE
    def test_author_can_update_their_own_flashcard(self, create_private_flashcard, create_private_flashcard_stack, authenticated_client):
        new_data = self.create_flashcard_data.copy()
        new_data['stack_id'] = create_private_flashcard_stack.id
        new_data['question'] = 'brobeans'
        response = authenticated_client.put(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', data=new_data, format='json')
        assert response.status_code == 200
        assert response.data['question'] == 'brobeans'

    def test_authenticated_cant_update_another_authors_flashcard(self, create_private_flashcard_stack, create_private_flashcard, authenticated_client2):
        new_data = self.create_flashcard_data.copy()
        new_data['stack_id'] = create_private_flashcard_stack.id
        new_data['question'] = 'brobeans'
        response = authenticated_client2.put(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', data=new_data, format='json')
        assert response.status_code == 403

    def test_unauthenticated_can_update_flashcard(self, create_private_flashcard_stack, create_private_flashcard):
        response = APIClient().put(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', data=self.create_flashcard_data, format='json')
        assert response.status_code == 401

    def test_updated_flashcard_gets_updated_date_modified(self, create_private_flashcard, create_private_flashcard_stack, authenticated_client):
        new_data = self.create_flashcard_data.copy()
        new_data['stack_id'] = create_private_flashcard_stack.id
        response = authenticated_client.put(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', data=new_data, format='json')
        assert response.status_code == 200
        assert response.data['date_modified'] != create_private_flashcard.date_modified

    # DELETE
    def test_author_can_delete_their_own_flashcard(self, create_private_flashcard, authenticated_client):
        response = authenticated_client.delete(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', format='json')
        assert response.status_code == 204
        assert Flashcard.objects.count() == 0

    def test_unautheticated_cant_delete_a_flashcard(self, create_private_flashcard):
        response = APIClient().delete(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', format='json')
        assert response.status_code == 401
        assert Flashcard.objects.count() == 1

    def test_authorized_cant_delete_another_authors_flashcard(self, create_private_flashcard, authenticated_client2):
        response = authenticated_client2.delete(path=f'/api/flashcards/flashcards/detail/{create_private_flashcard.id}/', format='json')
        assert response.status_code == 403
        assert Flashcard.objects.count() == 1


@pytest.mark.django_db
class TestPriority(CommonData):
    # GET
    def test_priority_is_created_when_accessing_weighted_flashcard(self, create_public_flashcard_stack, create_public_flashcard, authenticated_client):
        assert Priority.objects.count() == 0
        response = authenticated_client.get(path=f'/api/flashcards/flashcards/weightedflashcard/{create_public_flashcard_stack.id}/', format='json')
        assert response.status_code == 200
        assert Priority.objects.count() == 1

    def test_priority_is_calculated_correctly(self, create_public_flashcard_stack, create_public_flashcard,
                                              authenticated_client, create_priority):
        response = authenticated_client.get(
            path=f'/api/flashcards/flashcards/weightedflashcard/{create_public_flashcard_stack.id}/', format='json')
        assert response.status_code == 200
        assert response.data['id'] == create_public_flashcard.id

    def test_unauthenticated_cant_access_weighted_api(self, create_private_flashcard_stack, authenticated_client):
        response = APIClient().get(
            path=f'/api/flashcards/flashcards/weightedflashcard/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 401

    def test_authenticated_can_access_weighted_api(self, create_priority, create_private_flashcard,
                                                   create_private_flashcard_stack, authenticated_client):
        response = authenticated_client.get(
            path=f'/api/flashcards/flashcards/weightedflashcard/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 200

    def test_weighted_api_returns_a_flashcard(self, create_priority, create_private_flashcard,
                                              create_private_flashcard_stack, authenticated_client):
        response = authenticated_client.get(
            path=f'/api/flashcards/flashcards/weightedflashcard/{create_private_flashcard_stack.id}/', format='json')
        assert response.status_code == 200
        assert response.data['id'] == create_private_flashcard_stack.flashcards.all()[0].id

    # POST
    def test_authenticated_can_post_to_weighted_api(self, create_priority, create_public_flashcard, create_private_flashcard_stack, authenticated_client):
        data = {'id': create_priority.id, 'priority': 1, 'flashcard_id': create_public_flashcard.id}
        response = authenticated_client.post(
            path=f'/api/flashcards/flashcards/weightedflashcard/{create_private_flashcard_stack.id}/', data=data, format='json')
        assert response.status_code == 200
