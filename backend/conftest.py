import pytest

from rest_framework.test import APIClient
from flashcards.models import FlashcardStack, Flashcard, Priority
from django.contrib.auth.models import User


class CommonData:
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPassword',
        'password2': 'TestPassword',
    }
    login_user_data = {
        'username': user_data['username'],
        'password': user_data['password'],
    }
    create_user_data = {
        'username': user_data['username'],
        'email': user_data['email'],
        'password': user_data['password'],
    }
    create_public_flashcard_stack_data = {
        'public': True,
        'name': 'Test Flashcard Stack',
        'difficulty': 'easy',
    }
    create_private_flashcard_stack_data = {
        'public': False,
        'name': 'Test Flashcard Stack',
        'difficulty': 'easy',
    }


@pytest.fixture
def create_public_flashcard_stack(create_user):
    flashcard_stack_data = CommonData().create_public_flashcard_stack_data.copy()
    flashcard_stack = FlashcardStack.objects.create(
        author=create_user,
        **flashcard_stack_data
    )
    assert FlashcardStack.objects.count() >= 1
    return flashcard_stack


@pytest.fixture
def create_private_flashcard_stack(create_user):
    flashcard_stack_data = CommonData().create_private_flashcard_stack_data.copy()
    flashcard_stack = FlashcardStack.objects.create(
        author=create_user,
        **flashcard_stack_data
    )
    assert FlashcardStack.objects.count() >= 1
    return flashcard_stack


@pytest.fixture
def create_private_flashcard_stack2():
    user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')
    flashcard_stack_data = CommonData().create_private_flashcard_stack_data.copy()
    flashcard_stack = FlashcardStack.objects.create(
        author=user2,
        **flashcard_stack_data
    )
    assert FlashcardStack.objects.count() >= 1
    return flashcard_stack


@pytest.fixture
def create_user():
    user_data = CommonData().user_data.copy()
    user_data.pop('password2')

    user = User.objects.create_user(**user_data)
    assert User.objects.count() >= 1
    return user


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
    client.force_authenticate(user=create_user)
    return client