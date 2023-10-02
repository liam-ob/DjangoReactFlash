import pytest
import os

from PIL import Image
from rest_framework.test import APIClient
from flashcards.models import FlashcardStack, Flashcard, Priority
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings


class CommonData:
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPassword',
        'password2': 'TestPassword',
    }
    user_data2 = {
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'password',
        'password2': 'password',
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
    create_flashcard_data = {
        'question': 'Test question',
        'answer_char': 'Test answer',
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
def create_private_flashcard_stack2(create_user2):
    flashcard_stack_data = CommonData().create_private_flashcard_stack_data.copy()
    flashcard_stack = FlashcardStack.objects.create(
        author=create_user2,
        **flashcard_stack_data
    )
    assert FlashcardStack.objects.count() >= 1
    return flashcard_stack


@pytest.fixture
def create_user():
    user_data = CommonData().user_data.copy()
    user_data.pop('password2')

    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def create_user2():
    user_data = CommonData().user_data2.copy()
    user_data.pop('password2')

    user = User.objects.create_user(**user_data)
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


@pytest.fixture
def authenticated_client2(create_user2):
    data = CommonData().user_data2.copy()
    client = APIClient()
    client.post('/api/core/users/login/', data, format='json')
    client.force_authenticate(user=create_user2)
    return client


@pytest.fixture
def create_image():
    img = Image.new('RGB', (100, 100), (255, 255, 255))
    img_path = os.path.join(settings.MEDIA_ROOT, 'test.png')
    img.save(img_path)
    image_file = SimpleUploadedFile("test.png", open(img_path, 'rb').read(), content_type='image/png')
    yield image_file
    os.remove(os.path.join(settings.MEDIA_ROOT, 'images', 'test.png'))
    os.remove(img_path)


@pytest.fixture
def create_public_flashcard(create_public_flashcard_stack):
    flashcard_data = CommonData().create_flashcard_data.copy()
    flashcard_data['stack_id'] = create_public_flashcard_stack.id
    flashcard = Flashcard.objects.create(**flashcard_data)
    assert Flashcard.objects.count() >= 1
    return flashcard


@pytest.fixture
def create_private_flashcard(create_private_flashcard_stack):
    flashcard_data = CommonData().create_flashcard_data.copy()
    flashcard_data['stack_id'] = create_private_flashcard_stack.id
    flashcard = Flashcard.objects.create(**flashcard_data)
    assert Flashcard.objects.count() >= 1
    return flashcard


@pytest.fixture
def create_public_priority(create_user, create_public_flashcard):
    priority = Priority.objects.create(
        author=create_user,
        flashcard=create_public_flashcard,
        priority=9
    )
    return priority


@pytest.fixture
def create_private_priority(create_user, create_private_flashcard):
    priority = Priority.objects.create(
        author=create_user,
        flashcard=create_private_flashcard,
        priority=9
    )
    return priority
